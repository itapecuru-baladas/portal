import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from supabase import create_client
from PIL import Image
import io, httpx
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SEU_ID = int(os.getenv("SEU_ID", "0"))

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
CIDADE, NOME, DESCRICAO, FOTOS = range(4)
user_data_temp = {}

def aplicar_marca_dagua(img_bytes):
    base = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    try:
        marca = Image.open("watermark.png").convert("RGBA")
    except:
        marca = Image.open("../public/Logo_futurista_Itapecuru_Baladas.png").convert("RGBA")
    marca.thumbnail((int(base.width * 0.28), int(base.height * 0.28)))
    pos = (base.width - marca.width - 15, base.height - marca.height - 15)
    base.paste(marca, pos, marca)
    out = io.BytesIO()
    base.convert("RGB").save(out, format="JPEG", quality=85)
    out.seek(0)
    return out.getvalue()

async def start(update, context):
    await update.message.reply_text("Fala! Manda /novoevento pra criar galeria.")

async def novoevento(update, context):
    await update.message.reply_text("Qual a cidade? Ex: Itapecuru-Mirim")
    return CIDADE

async def receber_cidade(update, context):
    user_data_temp[update.effective_user.id] = {"cidade": update.message.text}
    await update.message.reply_text("Nome do evento?")
    return NOME

async def receber_nome(update, context):
    user_data_temp[update.effective_user.id]["nome"] = update.message.text
    await update.message.reply_text("Descrição curta?")
    return DESCRICAO

async def receber_descricao(update, context):
    user_data_temp[update.effective_user.id]["descricao"] = update.message.text
    dados = user_data_temp[update.effective_user.id]
    res = supabase.table("eventos").insert({"nome": dados["nome"], "cidade": dados["cidade"].lower().replace(" ", "-"), "descricao": dados["descricao"], "produtor_telegram_id": update.effective_user.id, "produtor_nome": update.effective_user.full_name, "status": "rascunho"}).execute()
    evento_id = res.data[0]["id"]
    user_data_temp[update.effective_user.id]["evento_id"] = evento_id
    await update.message.reply_text("Agora manda as FOTOS (pode mandar álbum). Quando acabar, /fim")
    return FOTOS

async def receber_fotos(update, context):
    evento_id = user_data_temp[update.effective_user.id]["evento_id"]
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    img_bytes = httpx.get(file.file_path).content
    img_watermark = aplicar_marca_dagua(img_bytes)
    nome_file = f"{evento_id}/{photo.file_id}.jpg"
    supabase.storage.from_("fotos-publicas").upload(nome_file, img_watermark, {"content-type": "image/jpeg", "upsert": "true"})
    url_pub = supabase.storage.from_("fotos-publicas").get_public_url(nome_file)
    supabase.table("fotos").insert({"evento_id": evento_id, "url_watermark": url_pub}).execute()
    await update.message.reply_text("Foto recebida ✅ manda mais ou /fim")
    return FOTOS

async def fim(update, context):
    dados = user_data_temp.get(update.effective_user.id)
    if SEU_ID:
        await context.bot.send_message(chat_id=SEU_ID, text=f"🔥 NOVA GALERIA: {dados['nome']} - {dados['cidade']}\nID: {dados['evento_id']}\nAprovar em: /admin")
    await update.message.reply_text("Galeria enviada pra aprovação!")
    return ConversationHandler.END

app = Application.builder().token(BOT_TOKEN).build()
conv = ConversationHandler(entry_points=[CommandHandler("novoevento", novoevento)], states={CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_cidade)], NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_nome)], DESCRICAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_descricao)], FOTOS: [MessageHandler(filters.PHOTO, receber_fotos), CommandHandler("fim", fim)]}, fallbacks=[])
app.add_handler(CommandHandler("start", start))
app.add_handler(conv)
print("Bot rodando...")
app.run_polling()
