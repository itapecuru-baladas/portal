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
            return titulo_original, f"{titulo_original} agita Itapecuru Mirim e regiao!"
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Reescreva para evitar plagio - Portal Itapecuru Balada. 
        Titulo original: {titulo_original} 
        Link: {link}
        Responda no formato:
        TITULO: novo titulo chamativo
        RESUMO: resumo 2 paragrafos jovem, estilo Itapecuru Balada"""
        response = model.generate_content(prompt)
        texto = response.text
        t_match = re.search(r'TITULO:\s*(.*)', texto)
        r_match = re.search(r'RESUMO:\s*(.*)', texto, re.DOTALL)
        novo = t_match.group(1).strip() if t_match else titulo_original
        resumo = r_match.group(1).strip() if r_match else texto[:300]
        return novo, resumo
    except Exception as e:
        print(f"Erro Gemini: {e}")
        return titulo_original, f"{titulo_original} promete movimentar a noite de Itapecuru!"

def buscar_noticias_musica():
    try:
        print("Buscando noticias com requests...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        recentes = supabase.table("noticias_musica").select("titulo, link, conteudo_original").order("created_at", desc=True).limit(50).execute()
        titulos_recentes = [r['titulo'] for r in recentes.data] if recentes.data else []
        links_originais = [r['conteudo_original'] for r in recentes.data] if recentes.data else []
        
        url_feed = "https://g1.globo.com/rss/g1/pop-arte/musica/"
        r = requests.get(url_feed, headers=headers, timeout=15)
        print(f"Status feed: {r.status_code}")
        feed = feedparser.parse(r.content)
        print(f"Feed achou {len(feed.entries)} noticias")

        for entry in feed.entries[:5]:
            titulo_original = entry.title.strip()
            link_original = entry.link.strip()
            
            # Evita duplicado pelo conteudo_original (link original)
            if titulo_original in links_originais or link_original in [d.get('conteudo_original') for d in recentes.data or []]:
                continue
            # Verifica se já existe esse link original no conteudo_original
            check = supabase.table("noticias_musica").select("id").eq("conteudo_original", link_original).execute()
            if check.data:
                print(f"Ja existe: {titulo_original[:40]}")
                continue

            print(f"Processando: {titulo_original[:60]}")
            novo_titulo, resumo = resumir_com_gemini(titulo_original, link_original)
            
            imagem_final = ""
            if hasattr(entry, 'enclosures') and entry.enclosures:
                imagem_final = entry.enclosures[0].href
            if not imagem_final:
                imagem_final = "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"

            # CORREÇÃO DA FONTE - CITA ORIGINAL
            if "g1.globo.com" in link_original:
                fonte_original = "G1"
            elif "rollingstone" in link_original.lower():
                fonte_original = "【entity-Rolling Stone¦canonical_name=Rolling Stone】"
            elif "【entity-gshow¦canonical_name=GShow】" in link_original:
                fonte_original = "【entity-GShow¦canonical_name=GShow】"
            elif "【entity-uol¦canonical_name=UOL】" in link_original:
                fonte_original = "【entity-UOL¦canonical_name=UOL】"
            else:
                fonte_original = "G1 - Pop e Arte"

            resumo_com_fonte = f"{resumo}\n\nVia: {fonte_original}"

            try:
                print(f"Salvando: {novo_titulo[:50]} | Fonte: {fonte_original}")
                result = supabase.table("noticias_musica").insert({
                    "titulo": novo_titulo,
                    "resumo": resumo_com_fonte,
                    "link": "",  # SEM LINK EXTERNO PRA NAO PERDER SEO
                    "fonte": fonte_original,  # CITA A FONTE ORIGINAL
                    "imagem_url": imagem_final,
                    "conteudo_original": link_original,  # Guarda o link original aqui, escondido
                    "titulo_hash": f"{int(time.time())}_{random.randint(1000,9999)}"
                }).execute()
                print(f"SALVO OK")
                time.sleep(1)
            except Exception as e:
                print(f"Erro salvar: {e}")

        print("Ciclo finalizado")
    except Exception as e:
        print(f"Erro GERAL noticias: {e}")
        import traceback
        traceback.print_exc()

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
    while True:
        try:
            app = Application.builder().token(TELEGRAM_TOKEN).build()
            try:
                await app.bot.delete_webhook(drop_pending_updates=True)
                print("✅ Webhook deletado - fila limpa")
            except Exception as e:
                print(f"Aviso webhook: {e}")
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
            print("🤖 Bot iniciando polling...")
            await app.updater.start_polling(drop_pending_updates=True)
            print("🤖 Bot rodando sem conflito!")
            await asyncio.Event().wait()
        except Exception as e:
            if "Conflict" in str(e):
                print(f"⚠️ Conflito, tentando em 10s: {e}")
                await asyncio.sleep(10)
            else:
                print(f"Erro bot: {e}")
                await asyncio.sleep(5)

def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == "__main__":
    threading.Thread(target=loop_noticias, daemon=True).start()
    threading.Thread(target=start_bot_thread, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)