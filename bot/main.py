import os
import re
import time
import feedparser
import google.generativeai as genai
from fastapi import FastAPI
from supabase import create_client, Client
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# ENV
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Modelo que você já tem liberado
MODEL = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL)

RSS_G1_MUSICA = "https://g1.globo.com/rss/g1/musica/"

def limpar_texto(texto: str) -> str:
    # REMOVE qualquer menção que o Gemini inventar de Itapecuru
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
    prompt = f"""
Você é editor do portal Itapecuru Baladas, mas está escrevendo sobre música NACIONAL.
Tarefa: reescreva a notícia abaixo SEM adicionar cidade.

TÍTULO ORIGINAL: {titulo_original}
DESCRIÇÃO: {descricao_original}

Regras OBRIGATÓRIAS:
1. NÃO adicione "Itapecuru-Mirim", "Itapecuru", "Maranhão" ou qualquer cidade.
2. Título: reescreva curto, até 90 caracteres, chamativo, SEM cidade.
3. Resumo: 2 frases, até 180 caracteres, explicando a notícia, SEM "Confira os detalhes..." e SEM cidade.
4. Retorne APENAS JSON: {{"titulo": "...", "resumo": "..."}}

Exemplo: {{"titulo": "【entity-Oswaldo Montenegro¦canonical_name=Oswaldo Montenegro】 celebra 70 anos com turnê", "resumo": "Cantor revisita clássicos e apresenta músicas novas em shows pelo Brasil. Turnê passa por várias capitais."}}
"""
    try:
        resp = model.generate_content(prompt)
        text = resp.text.strip()
        # limpa ```json
        text = re.sub(r'```json|```', '', text).strip()
        import json
        data = json.loads(text)
        titulo = limpar_texto(data.get("titulo", titulo_original))[:120]
        resumo = limpar_texto(data.get("resumo", descricao_original))[:250]
        # garante que não são iguais
        if titulo == resumo:
            resumo = resumo[:120] + "..."
        return titulo, resumo
    except Exception as e:
        print(f"Erro Gemini: {e} - usando original")
        return limpar_texto(titulo_original)[:90], limpar_texto(descricao_original)[:180]

def buscar_e_salvar_noticias():
    feed = feedparser.parse(RSS_G1_MUSICA)
    salvas = 0
    for entry in feed.entries[:6]:
        link_real = entry.link
        titulo_orig = entry.title
        desc_orig = entry.get("summary", "")[:300]

        # verifica se já existe
        existe = supabase.table("noticias_musica").select("id").eq("link", link_real).execute()
        if len(existe.data) > 0:
            continue
        existe2 = supabase.table("noticias_musica").select("id").eq("conteudo_original", link_real).execute()
        if len(existe2.data) > 0:
            continue

        titulo, resumo = gerar_resumo_com_gemini(titulo_orig, desc_orig)
        imagem = extrair_imagem(link_real)

        print(f"Salvando: {titulo} -> {link_real}")

        supabase.table("noticias_musica").insert({
            "titulo": titulo,
            "resumo": resumo,
            "link": link_real,  # NUNCA EMPTY!
            "conteudo_original": link_real,
            "fonte": "G1",
            "imagem_url": imagem,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        salvas += 1
        time.sleep(1) # evita rate limit

    return salvas

@app.get("/")
def home():
    return {"status": "bot online", "model": MODEL}

@app.get("/forcar-noticias")
def forcar_noticias():
    try:
        total = buscar_e_salvar_noticias()
        return {"status": "rodou", "total": total, "model": MODEL}
    except Exception as e:
        return {"status": "erro", "erro": str(e)}

@app.get("/health")
def health():
    return {"ok": True}