import feedparser
from supabase import create_client
import os

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

# RSS de música
feeds = [
  "https://g1.globo.com/rss/g1/pop-arte/musica/",
  "https://rollingstone.com.br/feed/",
  "https://www.vagalume.com.br/news/feed/"
]

for feed_url in feeds:
  feed = feedparser.parse(feed_url)
  for entry in feed.entries[:5]:
    supabase.table("noticias_musica").upsert({
      "titulo": entry.title,
      "resumo": entry.summary[:200] if hasattr(entry, 'summary') else "",
      "link": entry.link,
      "imagem_url": entry.get("media_content", [{}])[0].get("url", ""),
      "fonte": "【entity-Rolling Stone¦canonical_name=Rolling Stone】 / G1",
      "categoria": "nacional"
    }, on_conflict="link").execute()