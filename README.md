# Portal Limpo - Itapecuru Baladas v2.0

Portal refatorado do zero para corrigir PGRST205 e cache.

## O que foi corrigido
- Novo endpoint `/api/noticias` que busca no Supabase no SERVER (não no client)
- Deduplicação por título
- Resumo limpo sem "Via:", "Confira..."
- Fonte apenas como TEXTO, sem link externo (requisito)
- Cache desativado: force-dynamic + no-store
- MundoMusicaSection busca de /api/noticias e não direto do Supabase

## Deploy na Vercel
1. Suba esses arquivos para https://github.com/itapecuru-baladas/portal
2. Na Vercel, adicione as 3 ENV vars:
   - NEXT_PUBLIC_SUPABASE_URL
   - NEXT_PUBLIC_SUPABASE_ANON_KEY
   - SUPABASE_SERVICE_ROLE_KEY
3. Deploy com Clear Cache

## Teste
- /api/noticias deve retornar JSON array
- Home deve mostrar Mundo da Música sem links externos

## Bot
Não incluso, pois já está funcionando no Render.
