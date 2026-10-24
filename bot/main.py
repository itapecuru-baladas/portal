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
        return