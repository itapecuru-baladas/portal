import os, asyncio, threading
from flask import Flask
from supabase import create_client
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

flask_app = Flask(__name__)
@flask_app.route("/")
def health(): return "Bot Itapecuru Baladas - OK! LIVE"

# Estados
PERGUNTA_TIPO, NOME_EVENTO, DATA_EVENTO, HORARIO_EVENTO, ATRACOES, NOME_FOTOGRAFO, EVENTO_GALERIA, WHATS_FOTOGRAFO = range(8)

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
    draw.text((w-300, h+20), "PUBLICIDADE AQUI →", font=font_pequena, fill=(255,255,0,200))
    return nova_img.convert("RGB")

user_photos = {}

async def handle_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    caminho_temp = f"temp_{update.effective_user.id}.jpg"
    await file.download_to_drive(caminho_temp)
    user_photos[update.effective_user.id] = caminho_temp
    await update.message.reply_text(
        "📸 Foto recebida!\n\nO que é isso?\n\n1️⃣ - CARTAZ DE FESTA\n2️⃣ - FOTO DE GALERIA / FOTÓGRAFO\n\nDigite 1 ou 2"
    )
    return PERGUNTA_TIPO

async def pergunta_tipo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    if texto == "1":
        await update.message.reply_text("🎉 CARTAZ! Qual o NOME DO EVENTO?")
        return NOME_EVENTO
    else:
        await update.message.reply_text("📷 FOTO DE GALERIA!\n\nQual seu NOME / NOME DO FOTÓGRAFO?")
        return NOME_FOTOGRAFO

# --- FLUXO CARTAZ ---
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
    supabase.table("eventos").insert({
        "nome": context.user_data['nome_evento'],
        "data_evento": context.user_data['data'],
        "local": f"{context.user_data['horario']} - {context.user_data['atracoes']}",
        "capa_url": url, "slug": slug, "status": "publicado"
    }).execute()
    await update.message.reply_text(f"✅ CARTAZ CADASTRADO!\n\nEvento: {context.user_data['nome_evento']}\nJá está no site!")
    return ConversationHandler.END

# --- FLUXO FOTÓGRAFO ---
async def nome_fotografo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fotografo'] = update.message.text
    await update.message.reply_text(f"Valeu, {update.message.text}! 📸\n\nQual o NOME DO EVENTO / FESTA dessas fotos?")
    return EVENTO_GALERIA

async def evento_galeria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['evento_galeria'] = update.message.text
    await update.message.reply_text("📱 Qual seu WHATSAPP para crédito? (opcional, pode pular digitando 'pular')")
    return WHATS_FOTOGRAFO

async def whats_fotografo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    whatsapp = "" if "pular" in update.message.text.lower() else update.message.text
    caminho = user_photos.get(update.effective_user.id)
    final = aplica_marca_dagua_com_publicidade(caminho)
    final.save("final.jpg")
    nome = f"galeria_{int(datetime.now().timestamp())}.jpg"
    supabase.storage.from_("fotos-publicas").upload(nome, open("final.jpg","rb"), {"content-type":"image/jpeg", "upsert":"true"})
    url = supabase.storage.from_("fotos-publicas").get_public_url(nome)
    
    supabase.table("fotos").insert({
        "url": url,
        "fotografo": context.user_data['fotografo'],
        "evento_nome": context.user_data['evento_galeria'],
        "whatsapp": whatsapp,
        "tipo": "galeria"
    }).execute()
    
    await update.message.reply_text(
        f"✅ FOTO PUBLICADA!\n\n"
        f"📸 Fotógrafo: {context.user_data['fotografo']}\n"
        f"🎉 Evento: {context.user_data['evento_galeria']}\n"
        f"Com logo + espaço para publicidade!"
    )
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
    threading.Thread(target=start_bot_thread, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)