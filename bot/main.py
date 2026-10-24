import os
import asyncio
import threading
import time
import random
import requests
import re
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
def health():
    return "Bot Itapecuru Baladas - Telegram + Noticias Gemini LIVE - OK"

@flask_app.route("/forcar-noticias")
def forcar_noticias():
    try:
        buscar_noticias_musica()
        data = supabase.table("noticias_musica").select("*").order("created_at", desc=True).limit(3).execute()
        return {"status": "rodou", "total": len(data.data), "noticias": data.data}
    except Exception as e:
        return {"erro": str(e)}

def titulos_parecidos(t1, t2):
    return SequenceMatcher(None, t1.lower(), t2.lower()).ratio() > 0.8

def aplica_marca_dagua(caminho):
    img = Image.open(caminho).convert("RGB")
    w, h = img.size
    barra = 140
    nova = Image.new("RGB", (w, h+barra), (0,0,0))
    nova.paste(img, (0,0))
    draw = ImageDraw.Draw(nova)
    font = ImageFont.load_default()
    draw.text((20, h-40), "ITAPECURU BALADA", font=font, fill=(255,255,255))
    draw.text((20, h+10), "@itapecurubalada.com.br", font=font, fill=(255,255,255))
    draw.text((w-200, h+10), "PUBLICIDADE", font=font, fill=(255,255,0))
    return nova

def parse_data(texto):
    try:
        if "/" in texto:
            partes = texto.split("/")
            d = partes[0].zfill(2)
            m = partes[1].zfill(2)
            y = partes[2]
            return f"{y}-{m}-{d}"
        return texto
    except:
        return datetime.now().date().isoformat()

def resumir_com_gemini(titulo_original, link):
    try:
        if not GEMINI_KEY:
            return titulo_original, f"{titulo_original} agita Itapecuru!"
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Reescreva para evitar plagio - Portal Itapecuru Balada. Titulo: {titulo_original} Link: {link}. Responda: TITULO: novo titulo RESUMO: resumo 2 paragrafos jovem"
        response = model.generate_content(prompt)
        texto = response.text
        t_match = re.search(r'TITULO:\s*(.*)', texto)
        r_match = re.search(r'RESUMO:\s*(.*)', texto, re.DOTALL)
        novo = t_match.group(1).strip() if t_match else titulo_original
        resumo = r_match.group(1).strip() if r_match else texto[:300]
        return novo, resumo
    except Exception as e:
        print(f"Erro Gemini: {e}")
        return titulo_original, f"{titulo_original} promete movimentar Itapecuru!"

def buscar_noticias_musica():
    try:
        print("Buscando noticias...")
        feeds = ["https://g1.globo.com/rss/g1/pop-arte/musica/"]
        recentes = supabase.table("noticias_musica").select("titulo, link").order("created_at", desc=True).limit(50).execute()
        titulos_recentes = [r['titulo'] for r in recentes.data] if recentes.data else []
        links_recentes = [r['link'] for r in recentes.data] if recentes.data else []
        for feed_url in feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                titulo_original = entry.title.strip()
                link_original = entry.link.strip()
                if link_original in links_recentes:
                    continue
                repetido = False
                for t in titulos_recentes:
                    if titulos_parecidos(titulo_original, t):
                        repetido = True
                        break
                if repetido:
                    continue
                print(f"Nova: {titulo_original}")
                imagem_url = ""
                if hasattr(entry, 'enclosures') and entry.enclosures:
                    imagem_url = entry.enclosures[0].href
                novo_titulo, resumo = resumir_com_gemini(titulo_original, link_original)
                imagem_final = imagem_url
                if imagem_url:
                    try:
                        img_data = requests.get(imagem_url, timeout=10).content
                        nome_img = f"noticia_{int(time.time())}_{random.randint(1000,9999)}.jpg"
                        supabase.storage.from_("fotos-publicas").upload(nome_img, img_data, {"content-type":"image/jpeg","upsert":"true"})
                        imagem_final = supabase.storage.from_("fotos-publicas").get_public_url(nome_img)
                    except Exception as ex:
                        print(f"Erro imagem: {ex}")
                        imagem_final = imagem_url
                try:
                    supabase.table("noticias_musica").insert({
                        "titulo": novo_titulo,
                        "resumo": resumo,
                        "link": link_original,
                        "fonte": "Itapecuru Balada",
                        "imagem_url": imagem_final,
                        "conteudo_original": titulo_original,
                        "titulo_hash": novo_titulo.lower()[:50]
                    }).execute()
                    titulos_recentes.append(novo_titulo)
                    links_recentes.append(link_original)
                    print(f"Salvo: {novo_titulo}")
                except Exception as e:
                    print(f"Erro salvar: {e}")
                time.sleep(5)
        print("Ciclo finalizado")
    except Exception as e:
        print(f"Erro noticias: {e}")

def loop_noticias():
    while True:
        buscar_noticias_musica()
        time.sleep(10800)

PERGUNTA_TIPO, NOME_EVENTO, DATA_EVENTO, HORARIO_EVENTO, ATRACOES, NOME_FOTOGRAFO, EVENTO_GALERIA, WHATS_FOTOGRAFO = range(8)
user_photos = {}

async def handle_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    caminho_temp = f"temp_{update.effective_user.id}.jpg"
    await file.download_to_drive(caminho_temp)
    user_photos[update.effective_user.id] = caminho_temp
    await update.message.reply_text("Foto recebida! O que e? 1 - CARTAZ DE FESTA 2 - FOTO GALERIA Digite 1 ou 2")
    return PERGUNTA_TIPO

async def pergunta_tipo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.strip() == "1":
        await update.message.reply_text("Nome do evento?")
        return NOME_EVENTO
    else:
        await update.message.reply_text("Seu nome / fotografo?")
        return NOME_FOTOGRAFO

async def nome_evento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nome_evento'] = update.message.text
    await update.message.reply_text("Data? ex 25/10/2026")
    return DATA_EVENTO

async def data_evento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['data'] = update.message.text
    await update.message.reply_text("Horario? ex 22h")
    return HORARIO_EVENTO

async def horario_evento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['horario'] = update.message.text
    await update.message.reply_text("Atracoes?")
    return ATRACOES

async def atracoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['atracoes'] = update.message.text
    caminho = user_photos.get(update.effective_user.id)
    final = aplica_marca_dagua(caminho)
    final.save("final.jpg")
    nome = f"cartaz_{int(time.time())}.jpg"
    with open("final.jpg","rb") as f:
        supabase.storage.from_("fotos-publicas").upload(nome, f.read(), {"content-type":"image/jpeg","upsert":"true"})
    url = supabase.storage.from_("fotos-publicas").get_public_url(nome)
    slug = context.user_data['nome_evento'].lower().replace(" ","-")+"-"+str(int(time.time()))
    data_iso = parse_data(context.user_data['data'])
    supabase.table("eventos").insert({"nome": context.user_data['nome_evento'], "data_evento": data_iso, "local": f"{context.user_data['horario']} - {context.user_data['atracoes']}", "capa_url": url, "slug": slug, "status": "publicado"}).execute()
    await update.message.reply_text(f"Cartaz cadastrado! {context.user_data['nome_evento']}")
    return ConversationHandler.END

async def nome_fotografo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fotografo'] = update.message.text
    await update.message.reply_text(f"Valeu {update.message.text}! Nome do evento?")
    return EVENTO_GALERIA

async def evento_galeria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['evento_galeria'] = update.message.text
    await update.message.reply_text("Whatsapp? ou pular")
    return WHATS_FOTOGRAFO

async def whats_fotografo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    whatsapp = "" if "pular" in update.message.text.lower() else update.message.text
    caminho = user_photos.get(update.effective_user.id)
    final = aplica_marca_dagua(caminho)
    final.save("final.jpg")
    nome = f"galeria_{int(time.time())}.jpg"
    with open("final.jpg","rb") as f:
        supabase.storage.from_("fotos-publicas").upload(nome, f.read(), {"content-type":"image/jpeg","upsert":"true"})
    url = supabase.storage.from_("fotos-publicas").get_public_url(nome)
    supabase.table("fotos").insert({"url": url, "fotografo": context.user_data['fotografo'], "evento_nome": context.user_data['evento_galeria'], "whatsapp": whatsapp, "tipo": "galeria"}).execute()
    await update.message.reply_text(f"Foto publicada! {context.user_data['fotografo']}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelado.")
    return ConversationHandler.END

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    try:
        await app.bot.delete_webhook(drop_pending_updates=True)
        print("Webhook deletado")
    except Exception as e:
        print(f"Aviso: {e}")
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
    await app.updater.start_polling(drop_pending_updates=True)
    print("Bot rodando!")
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