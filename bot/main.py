import os, asyncio, threading, time, random, requests, re
from flask import Flask
from supabase import create_client
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from difflib import SequenceMatcher
import feedparser
import google.generativeai as genai

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

flask_app = Flask(__name__)
@flask_app.route("/")
def health(): return "Bot Itapecuru Baladas - Telegram + Noticias Gemini LIVE - OK"

# ================= FUNÇÕES AUXILIARES =================
def titulos_parecidos(t1, t2):
    return SequenceMatcher(None, t1.lower(), t2.lower()).ratio() > 0.8

def aplica_marca_dagua_com_publicidade(caminho):
    img = Image.open(caminho).convert("RGBA")
    w, h = img.size
    barra_altura = 140
    nova_altura = h + barra_altura
    nova_img = Image.new("RGBA", (w, nova_altura), (0,0,0,255))
    nova_img.paste(img, (0,0))
    draw = ImageDraw.Draw(nova_img)
    try: 
        font_grande = ImageFont.truetype("arial.ttf", 40)
        font_pequena = ImageFont.truetype("arial.ttf", 22)
    except: 
        font_grande = ImageFont.load_default()
        font_pequena = ImageFont.load_default()
    draw.text((20, h-50), "ITAPECURU BALADA", font=font_grande, fill=(255,255,255,200))
    draw.text((20, h+20), "@itapecurubalada.com.br", font=font_pequena, fill=(255,255,255,180))
    draw.text((w-300, h+20), "PUBLICIDADE AQUI", font=font_pequena, fill=(255,255,0,200))
    return nova_img.convert("RGB")

def parse_data(texto):
    try:
        if "/" in texto:
            d,m,y = texto.split("/")[:3]
            return f"{y}-{m.zfill(2)}-{d.zfill(2)}"
        return texto
    except:
        return datetime.now().isoformat()

def resumir_com_gemini(titulo_original, link):
    try:
        if not GEMINI_KEY:
            return f"{titulo_original} agita Itapecuru!", f"{titulo_original} está dando o que falar no mundo da música e promete agitar a cena de Itapecuru Mirim!"
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Você é redator do portal Itapecuru Balada, Maranhão.
        Reescreva essa notícia de música para evitar plágio (anti-strike Google):
        Título original: {titulo_original}
        Link: {link}
        Faça:
        1. Novo título chamativo (máx 80 caracteres)
        2. Resumo de 2 parágrafos, estilo fofoca/pop, jovem do MA
        Responda no formato:
        TITULO: seu título
        RESUMO: seu resumo
        """
        response = model.generate_content(prompt)
        texto = response.text
        titulo_match = re.search(r'TITULO:\s*(.*)', texto)
        resumo_match = re.search(r'RESUMO:\s*(.*)', texto, re.DOTALL)
        novo_titulo = titulo_match.group(1).strip() if titulo_match else titulo_original
        resumo = resumo_match.group(1).strip() if resumo_match else texto[:300]
        return novo_titulo, resumo
    except Exception as e:
        print(f"Erro Gemini: {e}")
        return titulo_original, f"{titulo_original} promete movimentar a noite de Itapecuru!"

# ================= BOT DE NOTICIAS ANTI-REPETIÇÃO + GEMINI + IMAGEM =================
def buscar_noticias_musica():
    try:
        print("🔍 Buscando notícias com Gemini anti-repetição...")
        feeds = ["https://g1.globo.com/rss/g1/pop-arte/musica/", "https://www.vagalume.com.br/news/index.xml"]
        recentes = supabase.table("noticias_musica").select("titulo, link").order("created_at", desc=True).limit(50).execute()
        titulos_recentes = [r['titulo'] for r in recentes.data] if recentes.data else []
        links_recentes = [r['link'] for r in recentes.data] if recentes.data else []

        for feed_url in feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                titulo_original = entry.title.strip()
                link_original = entry.link.strip()
                if link_original in links_recentes:
                    print(f"⏭️ Link repetido: {titulo_original}")
                    continue
                repetido = False
                for t_recente in titulos_recentes:
                    if titulos_parecidos(titulo_original, t_recente):
                        print(f"⏭️ Título parecido: {titulo_original} ~ {t_recente}")
                        repetido = True
                        break
                if repetido: continue
                existe = supabase.table("noticias_musica").select("id").eq("conteudo_original", titulo_original).execute()
                if existe.data:
                    print(f"⏭️ Conteúdo original já existe: {titulo_original}")
                    continue
                print(f"✅ Nova: {titulo_original}")
                imagem_url = ""
                if 'media_content' in entry: imagem_url = entry.media_content[0]['url']
                elif 'enclosures' in entry and entry.enclosures: imagem_url = entry.enclosures[0].href
                novo_titulo, resumo = resumir_com_gemini(titulo_original, link_original)
                for t_recente in titulos_recentes:
                    if titulos_parecidos(novo_titulo, t_recente):
                        print(f"⏭️ Gemini gerou título repetido: {novo_titulo}")
                        repetido = True
                        break
                if repetido: continue
                imagem_final = imagem_url
                if imagem_url:
                    try:
                        img_data = requests.get(imagem_url, timeout=10).content
                        nome_img = f"noticia_{int(datetime.now().timestamp())}_{random.randint(1000,9999)}.jpg"
                        supabase.storage.from_("fotos-publicas").upload(nome_img, img_data, {"content-type":"image/jpeg", "upsert":"true"})
                        imagem_final = supabase.storage.from_("fotos-publicas").get_public_url(nome_img)
                    except: imagem_final = imagem_url
                try:
                    supabase.table("noticias_musica").insert({
                        "titulo": novo_titulo, "resumo": resumo, "link": link_original,
                        "fonte": "Itapecuru Balada", "imagem_url": imagem_final,
                        "conteudo_original": titulo_original, "titulo_hash": novo_titulo.lower()[:50]
                    }).execute()
                    titulos_recentes.append(novo_titulo)
                    links_recentes.append(link_original)
                    print(f"✅ Salvo: {novo_titulo}")
                except Exception as e:
                    if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                        print(f"⏭️ Bloqueado pelo banco (duplicado): {novo_titulo}")
                    else: print(f"Erro ao salvar: {e}")
                time.sleep(8)
        print("✅ Ciclo notícias finalizado!")
    except Exception as e:
        print(f"Erro noticias: {e}")

def loop_noticias():
    while True:
        buscar_noticias_musica()
        time.sleep(3*60*60)

# ================= BOT TELEGRAM FOTÓGRAFO + CARTAZ =================
PERGUNTA_TIPO, NOME_EVENTO, DATA_EVENTO, HORARIO_EVENTO, ATRACOES, NOME_FOTOGRAFO, EVENTO_GALERIA, WHATS_FOTOGRAFO = range(8)
user_photos = {}

async def handle_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    caminho_temp = f"temp_{update.effective_user.id}.jpg"
    await file.download_to_drive(caminho_temp)
    user_photos[update.effective_user.id] = caminho_temp
    await update.message.reply_text("📸 Foto recebida!\n\nO que é?\n1️⃣ - CARTAZ DE FESTA\n2️⃣ - FOTO DE GALERIA / FOTÓGRAFO\n\nDigite 1 ou 2")
    return PERGUNTA_TIPO

async def pergunta_tipo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.strip() == "1":
        await update.message.reply_text("🎉 CARTAZ! Qual o NOME DO EVENTO?")
        return NOME_EVENTO
    else:
        await update.message.reply_text("📷 FOTO DE GALERIA!\nQual seu NOME / NOME DO FOTÓGRAFO?")
        return NOME_FOTOGRAFO

async def nome_evento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nome_evento'] = update.message.text
    await update.message.reply_text("📅 DATA? (ex: 25/10/2026)")
    return DATA_EVENTO
async def data_evento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['data'] = update.message.text
    await update.message.reply_text("⏰ HORÁRIO? (ex: 22h)")
    return HORARIO_EVENTO
async def horario_evento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['horario'] = update.message.text
    await update.message.reply_text("🎤 ATRAÇÕES? (ex: 【entity-Wesley Safadão¦canonical_name=Wesley Safadão】, 【entity-Zé Vaqueiro¦canonical_name=Zé Vaqueiro】)")
    return ATRACOES
async def atracoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['atracoes'] = update.message.text
    caminho = user_photos.get(update.effective_user.id)
    final = aplica_marca_dagua_com_publicidade(caminho)
    final.save("final.jpg")
    nome = f"cartaz_{int(datetime.now().timestamp())}.jpg"
    supabase.storage.from_("fotos-publicas").upload(nome, open("final.jpg","rb"), {"content-type":"image/jpeg", "upsert":"true"})
    url = supabase.storage.from_("fotos-publicas").get_public_url(nome)
    slug = context.user_data['nome_evento'].lower().replace(" ","-")+"-"+str(int(datetime.now().timestamp()))
    data_iso = parse_data(context.user_data['data'])
    supabase.table("eventos").insert({"nome": context.user_data['nome_evento'], "data_evento": data_iso, "local": f"{context.user_data['horario']} - {context.user_data['atracoes']}", "capa_url": url, "slug": slug, "status": "publicado"}).execute()
    await update.message.reply_text(f"✅ CARTAZ CADASTRADO!\nEvento: {context.user_data['nome_evento']} - {data_iso}\nJá está no site!")
    return ConversationHandler.END
async def nome_fotografo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fotografo'] = update.message.text
    await update.message.reply_text(f"Valeu, {update.message.text}! 📸\nQual o NOME DO EVENTO / FESTA?")
    return EVENTO_GALERIA
async def evento_galeria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['evento_galeria'] = update.message.text
    await update.message.reply_text("📱 WHATSAPP pra crédito? (ou digite 'pular')")
    return WHATS_FOTOGRAFO
async def whats_fotografo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    whatsapp = "" if "pular" in update.message.text.lower() else update.message.text
    caminho = user_photos.get(update.effective_user.id)
    final = aplica_marca_dagua_com_publicidade(caminho)
    final.save("final.jpg")
    nome = f"galeria_{int(datetime.now().timestamp())}.jpg"
    supabase.storage.from_("fotos-publicas").upload(nome, open("final.jpg","rb"), {"content-type":"image/jpeg", "upsert":"true"})
    url = supabase.storage.from_("fotos-publicas").get_public_url(nome)
    supabase.table("fotos").insert({"url": url, "fotografo": context.user_data['fotografo'], "evento_nome": context.user_data['evento_galeria'], "whatsapp": whatsapp, "tipo": "galeria"}).execute()
    await update.message.reply_text(f"✅ FOTO PUBLICADA!\n📸 Fotógrafo: {context.user_data['fotografo']}\n🎉 Evento: {context.user_data['evento_galeria']}\nCom logo + publicidade!")
    return ConversationHandler.END
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelado.")
    return ConversationHandler.END
async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.PHOTO, handle_foto)],
        states={
            PERGUNTA_TIPO: [MessageHandler(filters.TEXT & ~filters.COMMAND, pergunta_tipo)],
            NOME_EVENTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, nome_evento)],
            DATA_EVENTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, data_evento)],
            HORARIO_EVENTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, horario_evento)],
            ATRACOES: [MessageHandler(filters.TEXT & ~filters.COMMAND, atracoes)],
            NOME_FOTOGRAFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, nome_fotografo)],
            EVENTO_GALERIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, evento_galeria)],
            WHATS_FOTOGRAFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, whats_fotografo)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)]
    )
    app.add_handler(conv)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == "__main__":
    threading.Thread(target=loop_noticias, daemon=True).start()
    threading.Thread(target=start_bot_thread, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)