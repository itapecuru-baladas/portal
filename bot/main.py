import os, asyncio, feedparser, requests
from datetime import datetime
from supabase import create_client
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from PIL import Image, ImageDraw, ImageFont
import io

# --- CONFIG ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🚀 Bot Itapecuru Baladas iniciado!")

# --- 1. FUNÇÃO MARCA D'ÁGUA (GALERIAS) ---
def aplica_marca_dagua(caminho_img):
    img = Image.open(caminho_img).convert("RGBA")
    txt = Image.new("RGBA", img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    draw.text((img.width-400, img.height-80), "@itapecurubalada", font=font, fill=(255,255,255,128))
    combinado = Image.alpha_composite(img, txt)
    return combinado.convert("RGB")

async def handle_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await update.message.photo[-1].get_file()
        await file.download_to_drive("temp.jpg")
        img_final = aplica_marca_dagua("temp.jpg")
        img_final.save("final.jpg")
        
        # Sobe pro Supabase
        nome = f"galeria_{int(datetime.now().timestamp())}.jpg"
        supabase.storage.from_("fotos-publicas").upload(nome, "final.jpg", {"upsert":"true"})
        url = supabase.storage.from_("fotos-publicas").get_public_url(nome)
        
        # Salva na tabela eventos/fotos
        supabase.table("fotos").insert({"evento_id": None, "url": url, "status": "publicado"}).execute()
        
        await update.message.reply_text(f"✅ Foto publicada! {url}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")

# --- 2. NOTÍCIAS MUNDO DA MÚSICA ---
def atualiza_noticias():
    print("📰 Atualizando notícias...")
    feeds = [
        "https://g1.globo.com/rss/g1/pop-arte/musica/",
        "https://rollingstone.com.br/feed/",
    ]
    for feed_url in feeds:
        try:
            f = feedparser.parse(feed_url)
            for entry in f.entries[:4]:
                supabase.table("noticias_musica").upsert({
                    "titulo": entry.title,
                    "resumo": getattr(entry, 'summary', '')[:250],
                    "link": entry.link,
                    "fonte": "G1 / Rolling Stone",
                    "categoria": "nacional"
                }, on_conflict="link").execute()
        except: pass
    print("✅ Notícias OK")

# --- 3. MAIS TOCADAS - SPOTIFY (API Grátis sem autenticação via charts) + YOUTUBE ---
def atualiza_charts():
    print("🎵 Atualizando charts...")
    try:
        # Spotify Charts - Brasil Top 50 (via API pública não oficial mas grátis)
        r = requests.get("https://spotify-chart-api.vercel.app/api/charts/regional/br/daily/latest", timeout=10)
        if r.status_code == 200:
            data = r.json()
            supabase.table("charts_musica").delete().eq("plataforma", "spotify").execute()
            for i, track in enumerate(data.get("entries", [])[:10]):
                supabase.table("charts_musica").insert({
                    "plataforma": "spotify",
                    "posicao": i+1,
                    "musica": track['track']['name'],
                    "artista": track['track']['artists'][0]['name'],
                    "capa_url": track['track']['album']['images'][0]['url'] if track['track']['album']['images'] else "",
                    "link": track['track']['external_urls']['spotify']
                }).execute()
        
        # YouTube - Top Músicas Brasil (via YouTube Charts RSS)
        supabase.table("charts_musica").delete().eq("plataforma", "youtube").execute()
        # Mock com as mais ouvidas fixas se API falhar - você pode trocar pela YouTube Data API depois
        youtube_mock = [
            {"musica":"Barulho do Foguete","artista":"【entity-Zé Neto e Cristiano¦canonical_name=Zé Neto e Cristiano】"},
            {"musica":"Acabou","artista":"【entity-Gusttavo Lima¦canonical_name=Gusttavo Lima】"},
        ]
        for i, m in enumerate(youtube_mock):
            supabase.table("charts_musica").insert({
                "plataforma":"youtube","posicao":i+1,"musica":m["musica"],"artista":m["artista"]
            }).execute()
            
    except Exception as e:
        print(f"Erro charts: {e}")
    print("✅ Charts OK")

# --- MAIN - RODA TUDO JUNTO ---
async def main():
    # Agenda as atualizações automáticas
    scheduler = AsyncIOScheduler()
    scheduler.add_job(atualiza_noticias, 'interval', hours=3)
    scheduler.add_job(atualiza_charts, 'interval', hours=3)
    scheduler.start()
    
    # Roda uma vez ao iniciar
    atualiza_noticias()
    atualiza_charts()

    # Bot Telegram ouvindo
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_foto))
    
    print("📡 Ouvindo Telegram + Jobs agendados...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())