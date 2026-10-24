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
    return "Bot Itapecuru Baladas - OK - Gemini 2.0"

@flask_app.route("/forcar-noticias")
def forcar_noticias():
    try:
        buscar_noticias_musica()
        data = supabase.table("noticias_musica").select("*").order("created_at", desc=True).limit(3).execute()
        return {"status": "rodou", "total": len(data.data), "noticias": data.data}
    except Exception as e:
        return {"erro": str(e)}

@flask_app.route("/test-gemini")
def test_gemini():
    try:
        if not GEMINI_KEY:
            return {"ok": False, "erro": "SEM GEMINI_API_KEY"}
        genai.configure(api_key=GEMINI_KEY)
        modelos_disp = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    modelos_disp.append(m.name)
        except Exception as e:
            modelos_disp = [f"erro listar: {e}"]

        for model_name in ['models/gemini-2.0-flash', 'models/gemini-2.5-flash', 'models/gemini-flash-latest', 'models/gemini-1.5-flash-002', 'gemini-2.0-flash']:
            try:
                model = genai.GenerativeModel(model_name)
                resp = model.generate_content("Responda apenas: Gemini OK em Itapecuru Balada")
                return {"ok": True, "modelo_usado": model_name, "resposta": resp.text, "modelos_disponiveis": modelos_disp, "key_prefix": GEMINI_KEY[:10]+"..."}
            except Exception as e:
                last_err = str(e)
                continue
        return {"ok": False, "erro": last_err, "modelos_disponiveis": modelos_disp, "key_prefix": GEMINI_KEY[:10]+"..."}
    except Exception as e:
        return {"ok": False, "erro": str(e)}

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
            p = texto.split("/")
            return f"{p[2]}-{p[1].zfill(2)}-{p[0].zfill(2)}"
        return texto
    except:
        return datetime.now().date().isoformat()

def resumir_com_gemini(titulo_original, link):
    try:
        if not GEMINI_KEY or not GEMINI_KEY.startswith("AIza"):
            return titulo_original, f"{titulo_original} agita Itapecuru Mirim!"
        genai.configure(api_key=GEMINI_KEY)
        prompt = f"""Voce e redator do portal Itapecuru Balada - MA.
        Reescreva evitando plagio.
        Titulo: {titulo_original}
        Responda EXATAMENTE:
        TITULO: novo titulo curto chamativo
        RESUMO: 2 paragrafos jovem, local, sem repetir titulo
        """
        for model_name in ['models/gemini-2.0-flash', 'models/gemini-flash-latest', 'models/gemini-2.5-flash', 'gemini-2.0-flash']:
            try:
                model = genai.GenerativeModel(model_name)
                r = model.generate_content(prompt)
                texto = r.text
                t = re.search(r'TITULO:\s*(.*)', texto, re.I)
                res = re.search(r'RESUMO:\s*(.*)', texto, re.I | re.S)
                novo = t.group(1).strip() if t else titulo_original
                resumo = res.group(1).strip() if res else texto[:500]
                print(f"Gemini OK [{model_name}]: {novo[:60]}")
                return novo, resumo
            except Exception as e:
                print(f"Falha {model_name}: {e}")
                continue
        return titulo_original, f"{titulo_original} promete movimentar Itapecuru!"
    except Exception as e:
        print(f"Erro Gemini: {e}")
        return titulo_original, f"{titulo_original} em Itapecuru Mirim!"

def buscar_noticias_musica():
    try:
        print("Buscando noticias...")
        headers = {"User-Agent": "Mozilla/5.0"}
        url_feed = "https://g1.globo.com/rss/g1/pop-arte/musica/"
        r = requests.get(url_feed, headers=headers, timeout=15)
        feed = feedparser.parse(r.content)
        print(f"Feed: {len(feed.entries)} noticias")

        for entry in feed.entries[:6]:
            titulo_original = entry.title.strip()
            link_original = entry.link.strip()

            check = supabase.table("noticias_musica").select("id").eq("conteudo_original", link_original).execute()
            if check.data:
                print(f"Duplicado: {titulo_original[:40]}")
                continue

            novo_titulo, resumo = resumir_com_gemini(titulo_original, link_original)

            imagem_final = entry.enclosures[0].href if hasattr(entry, 'enclosures') and entry.enclosures else "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"

            if "g1.globo.com" in link_original:
                fonte_original = "G1"
            elif "rollingstone" in link_original.lower():
                fonte_original = " 【entity-Rolling Stone¦canonical_name=Rolling Stone】"
            else:
                fonte_original = "G1 - Pop e Arte"

            resumo_final = f"{resumo}\n\nVia: {fonte_original}"

            supabase.table("noticias_musica").insert({
                "titulo": novo_titulo,
                "resumo": resumo_final,
                "link": "",
                "fonte": fonte_original,
                "imagem_url": imagem_final,
                "conteudo_original": link_original,
                "titulo_hash": f"{int(time.time())}_{random.randint(1000,9999)}"
            }).execute()
            print(f"SALVO: {novo_titulo[:50]} | Fonte: {fonte_original}")
            time.sleep(1)
    except Exception as e:
        print(f"Erro buscar: {e}")
        import traceback; traceback.print_exc()

def loop_noticias():
    while True:
        buscar_noticias_musica()
        time.sleep(10800)

PERGUNTA_TIPO, NOME_EVENTO, DATA_EVENTO, HORARIO_EVENTO, ATRACOES, NOME_FOTOGRAFO, EVENTO_GALERIA, WHATS_FOTOGRAFO = range(8)
user_photos = {}

async def handle_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    caminho = f"temp_{update.effective_user.id}.jpg"
    await file.download_to_drive(caminho)
    user_photos[update.effective_user.id] = caminho
    await update.message.reply_text("Foto recebida!\n1 - CARTAZ DE FESTA\n2 - FOTO GALERIA\nDigite 1 ou 2")
    return PERGUNTA_TIPO

async def pergunta_tipo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return NOME_EVENTO if update.message.text.strip() == "1" else NOME_FOTOGRAFO

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
    supabase.table("eventos").insert({"nome": context.user_data['nome_evento'], "data_evento": parse_data(context.user_data['data']), "local": f"{context.user_data['horario']} - {context.user_data['atracoes']}", "capa_url": url, "slug": slug, "status": "publicado"}).execute()
    await update.message.reply_text(f"Cartaz cadastrado! {context.user_data['nome_evento']}")
    return ConversationHandler.END

async def nome_fotografo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fotografo'] = update.message.text
    await update.message.reply_text("Nome do evento da galeria?")
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
    await update.message.reply_text("Foto publicada!")
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
            except:
                pass
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
            print("Bot OK")
            await asyncio.Event().wait()
        except Exception as e:
            print(f"Erro bot: {e}")
            await asyncio.sleep(10 if "Conflict" in str(e) else 5)

def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == "__main__":
    threading.Thread(target=loop_noticias, daemon=True).start()
    threading.Thread(target=start_bot_thread, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)