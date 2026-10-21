# Itapecuru Baladas - Portal

Projeto pronto para GitHub -> Vercel (frontend) + Supabase (banco e storage) + Render (bot Python)

## Passos

1. **Supabase**: Crie projeto e rode o SQL de `supabase/schema.sql`. Crie buckets `fotos-originais` (private) e `fotos-publicas` (public)

2. **GitHub**: `git init`, `git add .`, `git commit -m "initial"`, `git push`

3. **Vercel**: Importe o repo, adicione env vars do .env.example, deploy

4. **Render**: New Web Service -> Root Directory `bot` -> Build `pip install -r requirements.txt` -> Start `python main.py` -> adicione env vars

5. **Cloudflare**: Quando comprar domínio .com.br, aponte NS para Cloudflare e adicione domínio na Vercel

## Estrutura

/app - Next.js App Router
/components - Header, Flyers, MundoMusica, Galerias, Ads
/lib - Supabase client
/bot - Bot Python com marca d'água
/public - logo e assets
