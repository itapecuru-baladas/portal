import os, asyncio, feedparser, requests
from datetime import datetime
from supabase import create_client
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from PIL import Image, ImageDraw, ImageFont
import io

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🚀 Bot Itapecuru Baladas iniciado!")

def aplica_marca_dagua(caminho):
    img = Image.open(caminho).convert("RGBA")
    txt = Image.new("RGBA", img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt)
    try: font = ImageFont.truetype("arial.ttf", 40)
    except: font = ImageFont.load_default()
    draw.text((img.width-400, img.height-80), "@itapecurubalada", font=font, fill=(255,255,255,128))
    return Image.alpha_composite(img, txt).convert("RGB")

async def handle_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await update.message.photo[-1].get_file()
        await file.download_to_drive("temp.jpg")
        final = aplica_marca_dagua("temp.jpg")
        final.save("final.jpg")
        nome = f"galeria_{int(datetime.now().timestamp())}.jpg"
        supabase.storage.from_("fotos-publicas").upload(nome, "final.jpg", {"upsert":"true"})
        url = supabase.storage.from_("fotos-publicas").get_public_url(nome)
        supabase.table("fotos").insert({"url": url, "status": "publicado"}).execute()
        await update.message.reply_text(f"✅ Publicada! {url}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")

def atualiza_noticias():
    print("📰 Atualizando notícias...")
    for feed_url in ["https://g1.globo.com/rss/g1/pop-arte/musica/", "https://rollingstone.com.br/feed/"]:
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

def atualiza_charts():
    print("🎵 Charts...")
    try:
        r = requests.get("https://spotify-chart-api.vercel.app/api/charts/regional/br/daily/latest", timeout=10)
        if r.status_code == 200:
            data = r.json()
            supabase.table("charts_musica").delete().eq("plataforma", "【entity-spotify¦canonical_name=Spotify】").execute()
            for i, track in enumerate(data.get("entries", [])[:10]):
                supabase.table("charts_musica").insert({
                    "plataforma": "【entity-spotify¦canonical_name=Spotify】", "posicao": i+1,
                    "musica": track['track']['name'],
                    "artista": track['track']['artists'][0]['name'],
                    "capa_url": track['track']['album']['images'][0]['url'] if track['track']['album']['images'] else "",
                    "link": track['track']['external_urls']['【entity-spotify¦canonical_name=Spotify】']
                }).execute()
    except Exception as e:
        print(f"Erro charts: {e}")

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(atualiza_noticias, 'interval', hours=3)
    scheduler.add_job(atualiza_charts, 'interval', hours=3)
    scheduler.start()
    atualiza_noticias(); atualiza_charts()
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_foto))
    print("📡 Ouvindo Telegram...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio; nest_asyncio.apply()
    asyncio.run(main())