import os
import asyncio
from supabase import create_client
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🚀 Bot Itapecuru Baladas iniciado!")

def aplica_marca_dagua(caminho):
    img = Image.open(caminho).convert("RGBA")
    txt = Image.new("RGBA", img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt)
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
    draw.text((img.width-350, img.height-60), "@itapecurubalada", font=font, fill=(255,255,255,180))
    return Image.alpha_composite(img, txt).convert("RGB")

async def handle_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await update.message.photo[-1].get_file()
        await file.download_to_drive("temp.jpg")
        final = aplica_marca_dagua("temp.jpg")
        final.save("final.jpg")
        nome = f"galeria_{int(datetime.now().timestamp())}.jpg"
        supabase.storage.from_("fotos-publicas").upload(nome, open("final.jpg","rb"), {"content-type":"image/jpeg"})
        url = supabase.storage.from_("fotos-publicas").get_public_url(nome)
        supabase.table("fotos").insert({"url": url}).execute()
        await update.message.reply_text(f"✅ Foto publicada! {url}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")
        print(e)

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_foto))
    print("📡 Ouvindo Telegram...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())