import os
import re
import time
import feedparser
import google.generativeai as genai
from fastapi import FastAPI
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json

SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL") or ""
SUPABASE_KEY = (
    os.getenv("SUPABASE_SERVICE_KEY") 
    or os.getenv("SUPABASE_KEY") 
    or os.getenv("SUPABASE_ANON_KEY")
    or os.getenv("VITE_SUPABASE_ANON_KEY")
    or ""
)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Erro supabase: {e}")

model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        print(f"Erro Gemini: {e}")

app = FastAPI()
MODEL = "gemini-2.5-flash"
RSS_G1_MUSICA = "https://g1.globo.com/rss/g1/musica/"

def limpar_texto(texto: str) -> str:
    if not texto:
        return ""
    texto = re.sub(r'<[^>]+>', ' ', texto)
    texto = texto.replace("&nbsp;", " ").replace("&amp;", "&")
    texto = re.sub(r'(?i)itapecuru.*?(mirim|baladas)?', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def extrair_imagem(link: str) -> str:
    try:
        r = requests.get(link, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
    except:
        pass
    return "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800"

def gerar_resumo_com_gemini(titulo_original: str, descricao_original: str):
    titulo_original = limpar_texto(titulo_original)
    descricao_original = limpar_texto(descricao_original)
    if not model:
        return titulo_original[:90], descricao_original[:180]
    prompt = f"""Você é editor do portal Itapecuru Baladas, mas está escrevendo sobre música NACIONAL.
Reescreva SEM adicionar cidade.
TÍTULO: {titulo_original}
DESCRIÇÃO: {descricao_original}
Regras: NÃO adicione Itapecuru. Título até 90 chars. Resumo 2 frases até 180 chars. Retorne APENAS JSON: {{"titulo": "...", "resumo": "..."}}"""
    try:
        resp = model.generate_content(prompt)
        text = re.sub(r'```json|```', '', resp.text.strip()).strip()
        data = json.loads(text)
        titulo = limpar_texto(data.get("titulo", titulo_original))[:120]
        resumo = limpar_texto(data.get("resumo", descricao_original))[:250]
        return titulo, resumo
    except Exception as e:
        print(f"Erro Gemini: {e}")
        return titulo_original[:90], descricao_original[:180]

def buscar_e_salvar_noticias(forcar=False):
    if not supabase:
        raise Exception("Supabase não configurado")
    feed = feedparser.parse(RSS_G1_MUSICA)
    print(f"RSS retornou {len(feed.entries)} entries")
    salvas = 0
    ignoradas = 0
    for entry in feed.entries[:10]:
        link_real = entry.link
        titulo_orig = entry.title
        desc_orig = entry.get("summary", "")[:500]

        if not forcar:
            existe = supabase.table("noticias_musica").select("id").eq("link", link_real).execute()
            if len(existe.data) > 0:
                ignoradas += 1
                continue

        titulo, resumo = gerar_resumo_com_gemini(titulo_orig, desc_orig)
        imagem = extrair_imagem(link_real)

        supabase.table("noticias_musica").insert({
            "titulo": titulo,
            "resumo": resumo,
            "link": link_real,
            "conteudo_original": link_real,
            "fonte": "G1",
            "imagem_url": imagem,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        salvas += 1
        time.sleep(1)
    return salvas, ignoradas, len(feed.entries)

@app.get("/")
def home():
    return {
        "status": "bot online" if supabase else "sem ENV",
        "model": MODEL,
        "env": {
            "supabase_url": "OK" if SUPABASE_URL else "FALTANDO",
            "supabase_key": "OK" if SUPABASE_KEY else "FALTANDO",
            "gemini": "OK" if GEMINI_API_KEY else "FALTANDO"
        }
    }

@app.get("/debug-feed")
def debug_feed():
    feed = feedparser.parse(RSS_G1_MUSICA)
    items = []
    for e in feed.entries[:6]:
        items.append({
            "title": e.title,
            "link": e.link,
            "summary": limpar_texto(e.get("summary", ""))[:200]
        })
    total_banco = 0
    try:
        total_banco = len(supabase.table("noticias_musica").select("id").execute().data)
    except:
        pass
    return {
        "rss_total": len(feed.entries),
        "rss_primeiros_6": items,
        "total_no_banco": total_banco
    }

@app.get("/forcar-noticias")
def forcar_noticias(forcar: bool = False):
    try:
        total, ignoradas, rss_total = buscar_e_salvar_noticias(forcar=forcar)
        return {
            "status": "rodou",
            "total": total,
            "rss_total": rss_total,
            "ignoradas_duplicadas": ignoradas,
            "model": MODEL
        }
    except Exception as e:
        return {"status": "erro", "erro": str(e)}

@app.get("/forcar-noticias-debug")
def forcar_noticias_debug():
    return forcar_noticias(forcar=True)

@app.get("/health")
def health():
    return {"ok": True}