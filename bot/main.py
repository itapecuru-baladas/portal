import os, re, time, feedparser, json, requests
import google.generativeai as genai
from fastapi import FastAPI
from datetime import datetime
from bs4 import BeautifulSoup

SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL") or ""
SUPABASE_KEY = (os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY") or os.getenv("VITE_SUPABASE_ANON_KEY") or "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    from supabase import create_client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

model = None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()
RSS_G1_MUSICA = "https://g1.globo.com/rss/g1/musica/"

def limpar_texto(texto: str) -> str:
    if not texto: return ""
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
        if og and og.get("content"): return og["content"]
    except: pass
    return "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800"

def gerar_resumo_com_gemini(titulo_original: str, descricao_original: str):
    titulo_original = limpar_texto(titulo_original)
    descricao_original = limpar_texto(descricao_original)
    if not model: return titulo_original[:90], descricao_original[:180]
    prompt = f'Reescreva SEM adicionar cidade. TÍTULO: {titulo_original} DESCRIÇÃO: {descricao_original} Retorne APENAS JSON: {{"titulo": "...", "resumo": "..."}}'
    try:
        resp = model.generate_content(prompt)
        text = re.sub(r'```json|```', '', resp.text.strip()).strip()
        data = json.loads(text)
        return limpar_texto(data.get("titulo", titulo_original))[:120], limpar_texto(data.get("resumo", descricao_original))[:250]
    except Exception as e:
        print(f"Erro Gemini: {e}")
        return titulo_original[:90], descricao_original[:180]

def buscar_e_salvar_noticias(forcar=False):
    if not supabase: raise Exception("Supabase não configurado")
    feed = feedparser.parse(RSS_G1_MUSICA)
    salvas = 0; ignoradas = 0
    for entry in feed.entries[:10]:
        link_real = entry.link
        if not forcar:
            existe = supabase.table("noticias_musica").select("id").eq("link", link_real).execute()
            if len(existe.data) > 0: ignoradas += 1; continue
        titulo, resumo = gerar_resumo_com_gemini(entry.title, entry.get("summary", "")[:500])
        imagem = extrair_imagem(link_real)
        supabase.table("noticias_musica").insert({"titulo": titulo, "resumo": resumo, "link": link_real, "conteudo_original": link_real, "fonte": "G1", "imagem_url": imagem, "created_at": datetime.utcnow().isoformat()}).execute()
        salvas += 1; time.sleep(1)
    return salvas, ignoradas, len(feed.entries)

@app.get("/")
def home(): return {"status": "bot online" if supabase else "sem ENV", "env": {"supabase_url": "OK" if SUPABASE_URL else "FALTANDO", "supabase_key": "OK" if SUPABASE_KEY else "FALTANDO", "gemini": "OK" if GEMINI_API_KEY else "FALTANDO"}}

@app.get("/forcar-noticias")
def forcar_noticias(forcar: bool = False):
    total, ignoradas, rss_total = buscar_e_salvar_noticias(forcar=forcar)
    return {"status": "rodou", "total": total, "rss_total": rss_total, "ignoradas_duplicadas": ignoradas}

@app.get("/health")
def health(): return {"ok": True}