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

# --- ENV COM FALLBACK (não crasha mais) ---
SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL") or ""
SUPABASE_KEY = (
    os.getenv("SUPABASE_SERVICE_KEY") 
    or os.getenv("SUPABASE_KEY") 
    or os.getenv("SUPABASE_ANON_KEY")
    or os.getenv("VITE_SUPABASE_ANON_KEY")
    or ""
)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""

print(f"ENV CHECK -> URL: {'OK' if SUPABASE_URL else 'FALTANDO'} | KEY: {'OK' if SUPABASE_KEY else 'FALTANDO'} | GEMINI: {'OK' if GEMINI_API_KEY else 'FALTANDO'}")

# --- SUPABASE LAZY ---
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase conectado!")
    except Exception as e:
        print(f"Erro ao criar supabase: {e}")

# --- GEMINI LAZY ---
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        print(f"Gemini conectado: gemini-2.5-flash")
    except Exception as e:
        print(f"Erro Gemini: {e}")

app = FastAPI()
MODEL = "gemini-2.5-flash"
RSS_G1_MUSICA = "https://g1.globo.com/rss/g1/musica/"

def limpar_texto(texto: str) -> str:
    """Remove HTML, Itapecuru inventado, espaços duplos"""
    if not texto:
        return ""
    # 1. Remove HTML <img>, <br>, <div>, etc
    texto = re.sub(r'<[^>]+>', ' ', texto)
    # 2. Remove entidades HTML
    texto = texto.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"')
    # 3. Remove menção inventada de Itapecuru
    texto = re.sub(r'(?i)itapecuru.*?(mirim|baladas)?', '', texto)
    # 4. Limpa espaços
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def extrair_imagem(link: str) -> str:
    try:
        r = requests.get(link, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        # fallback: primeira img da matéria
        img = soup.find("img")
        if img and img.get("src") and "http" in img["src"]:
            return img["src"]
    except Exception as e:
        print(f"Erro extrair imagem {link}: {e}")
    return "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800"

def gerar_resumo_com_gemini(titulo_original: str, descricao_original: str):
    # LIMPA HTML ANTES DE MANDAR PRO GEMINI (fix do <img src>)
    titulo_original = limpar_texto(titulo_original)
    descricao_original = limpar_texto(descricao_original)

    if not model:
        return titulo_original[:90], descricao_original[:180]
    
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
        text = re.sub(r'```json|```', '', resp.text.strip()).strip()
        data = json.loads(text)
        titulo = limpar_texto(data.get("titulo", titulo_original))[:120]
        resumo = limpar_texto(data.get("resumo", descricao_original))[:250]
        if titulo.lower() == resumo.lower():
            resumo = resumo[:120] + "..."
        return titulo, resumo
    except Exception as e:
        print(f"Erro Gemini: {e} - usando original")
        return titulo_original[:90], descricao_original[:180]

def buscar_e_salvar_noticias():
    if not supabase:
        raise Exception(f"Supabase não configurado. URL={'OK' if SUPABASE_URL else 'FALTA'} KEY={'OK' if SUPABASE_KEY else 'FALTA'}")
    
    feed = feedparser.parse(RSS_G1_MUSICA)
    salvas = 0
    for entry in feed.entries[:6]:
        link_real = entry.link
        titulo_orig = entry.title
        desc_orig = entry.get("summary", "")[:500]

        # verifica se já existe por link
        existe = supabase.table("noticias_musica").select("id").eq("link", link_real).execute()
        if len(existe.data) > 0:
            print(f"Já existe: {link_real}")
            continue
        try:
            existe2 = supabase.table("noticias_musica").select("id").eq("conteudo_original", link_real).execute()
            if len(existe2.data) > 0:
                continue
        except:
            pass

        titulo, resumo = gerar_resumo_com_gemini(titulo_orig, desc_orig)
        imagem = extrair_imagem(link_real)

        print(f"Salvando: {titulo} -> {link_real}")

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
        time.sleep(1.2)

    return salvas

@app.get("/")
def home():
    return {
        "status": "bot online" if supabase and model else "bot online mas sem ENV",
        "model": MODEL,
        "env": {
            "supabase_url": "OK" if SUPABASE_URL else "FALTANDO",
            "supabase_key": "OK" if SUPABASE_KEY else "FALTANDO",
            "gemini": "OK" if GEMINI_API_KEY else "FALTANDO"
        }
    }

@app.get("/forcar-noticias")
def forcar_noticias():
    try:
        total = buscar_e_salvar_noticias()
        return {"status": "rodou", "total": total, "model": MODEL}
    except Exception as e:
        print(f"ERRO /forcar-noticias: {e}")
        return {"status": "erro", "erro": str(e)}

@app.get("/health")
def health():
    return {"ok": True, "supabase": bool(supabase), "gemini": bool(model)}