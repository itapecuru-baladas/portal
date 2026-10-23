import os, asyncio, threading
from flask import Flask
from supabase import create_client
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

flask_app = Flask(__name__)
@flask_app.route("/")
def health():
    return "Bot Itapecuru Baladas - OK! 🤖 LIVE"

def aplica_marca_dagua(caminho):
    img = Image.open(caminho).convert("RGBA")
    txt = Image.new("RGBA", img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt)
    try: font = ImageFont.truetype("arial.ttf", 30)
    except: font = ImageFont.load_default()
    draw.text((img.width-350, img.height-60), "@itapecurubalada", font=font, fill=(255,255,255,180))
    return Image.alpha_composite(img, txt).convert("RGB")

async def handle_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await update.message.photo[-1].get_file()
        await file.download_to_drive("temp.jpg")
        final = aplica_marca_dagua("temp.jpg")
        final.save("final.jpg")
        nome = f"galeria_{int(datetime.now().timestamp())}.jpg"
        supabase.storage.from_("fotos-publicas").upload(nome, open("final.jpg","rb"), {"content-type":"image/jpeg", "upsert":"true"})
        url = supabase.storage.from_("fotos-publicas").get_public_url(nome)
        supabase.table("fotos").insert({"url": url}).execute()
        await update.message.reply_text(f"✅ Publicada no portal! {url}")
    except Exception as e:
        print(e)
        await update.message.reply_text(f"❌ Erro: {e}")

async def run_bot():
    print("📡 Iniciando bot Telegram...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_foto))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("✅ Bot ouvindo!")
    await asyncio.Event().wait()

def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == "__main__":
    # Bot roda em background
    threading.Thread(target=start_bot_thread, daemon=True).start()
    # Flask roda no principal e abre a porta pro Render
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Abrindo porta {port} pro Render...")
    flask_app.run(host="0.0.0.0", port=port)