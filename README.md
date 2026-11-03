# ITAPECURU BALADAS - Portal Oficial v2

![Logo](public/logo-original.png)

> **Registrando momentos, conectando pessoas.**

Portal reconstruído do zero, limpo, 100% baseado no padrão visual da logo oficial.

---

## 🎨 DESIGN SYSTEM - Padrão da Logo (OBRIGATÓRIO)

Tudo no site segue a logo enviada:

| Elemento | Valor |
|---|---|
| **Fundo** | `#000000` preto puro |
| **Branco** | `#FFFFFF` |
| **Azul Escuro** | `#0047BB` |
| **Azul Médio** | `#0077FF` |
| **Azul Claro** | `#00A6FF` |
| **Gradiente** | `linear-gradient(90deg, #0047BB → #00A6FF)` |
| **Fonte ITAPECURU** | `Orbitron` Bold - futurista reta |
| **Fonte BALADAS** | `Montserrat Extra Bold Italic` - inclinada 6deg |
| **Slogan** | `Inter` Light 300, tracking 0.3em |
| **Equalizador** | 8 barras arredondadas com gradiente vertical |
| **Swoosh/Raio** | Linha azul com corte diagonal |

```css
:root {
  --ib-black: #000000;
  --ib-white: #FFFFFF;
  --ib-blue-dark: #0047BB;
  --ib-blue-mid: #0077FF;
  --ib-blue-light: #00A6FF;
  --ib-gradient: linear-gradient(90deg, #0047BB, #00A6FF);
}
```

**Regras:**
- Header sempre preto com equalizador à direita
- Swoosh azul como divisor de seções
- Cards com border `white/10` e hover `blue/50`
- NUNCA usar outro azul fora do gradiente oficial

---

## 🚀 STACK

- Next.js 14 App Router + TypeScript
- Tailwind CSS (cores custom IB)
- Supabase (tabela `noticias`)
- Vercel (deploy)

---

## 📁 ESTRUTURA LIMPA

```
app/
  layout.tsx              # Metadata + favicon
  page.tsx                # Página principal
  globals.css             # Variáveis e classes .baladas-title, .futur-title, .ib-swoosh
  favicon.png             # Favicon automático do Next
  api/
    noticias/
      route.ts            # API que volta a listar notícias do Supabase (SEM DUPLICATAS)

components/
  Header.tsx              # Header preto com logo transparente + equalizador
  Hero.tsx                # Hero com título BALADAS em gradiente
  MundoMusicaSection.tsx  # Seção que estava quebrada - AGORA CORRIGIDA

public/
  logo.png                # Logo transparente (sem fundo preto) - USE ESTE
  logo-original.png       # Logo original com fundo preto
  favicon.ico             # Favicon multi-resolução
  favicon.png, favicon-16x16.png, favicon-32x32.png, favicon-48x48.png
  apple-touch-icon.png    # iOS
  icon-192.png, icon-512.png
  manifest.json
```

---

## 🔧 CONFIGURAR

1. **Env:**
```bash
cp .env.example .env.local
# Preencha:
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx
```

2. **Instalar e rodar:**
```bash
npm install
npm run dev
```

3. **Supabase - Tabela `noticias`:**
```sql
create table noticias (
  id uuid default gen_random_uuid() primary key,
  titulo text not null,
  resumo text,
  categoria text default 'MÚSICA',
  capa_url text,
  created_at timestamp default now(),
  fonte text
);
```

---

## 🐛 CORREÇÕES FEITAS (MundoMusicaSection)

**Antes:** Não listava, duplicava, cache travado, citação com link externo.

**Agora em `app/api/noticias/route.ts`:**
```ts
export const dynamic = "force-dynamic";
export const revalidate = 0; // sem cache na Vercel

// Deduplicação por título
const unique = Array.from(new Map(data.map(n => [n.titulo, n])).values());
return NextResponse.json(unique, { headers: { "Cache-Control": "no-store" } });
```

**Citação da fonte SEM link externo (exigido):**
```tsx
<span className="text-[11px] tracking-widest text-white/40">Fonte: Itapecuru Baladas</span>
```

---

## 📱 FAVICON PACK

Gerado a partir do equalizador da logo:

- `favicon.ico` (16,32,48)
- `favicon.png` + variações
- `apple-touch-icon.png` (180)
- `icon-192.png` e `icon-512.png` (PWA)
- `manifest.json` com theme_color #0047BB

Next.js 14 já lê `app/favicon.png` automaticamente.

---

## ▲ DEPLOY NA VERCEL

1. Push para GitHub
2. Vercel → New Project → Import GitHub repo
3. Adicione Environment Variables: `NEXT_PUBLIC_SUPABASE_URL` e `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. Deploy

---

## ✅ CHECKLIST FINAL

- [x] Logo transparente em `public/logo.png`
- [x] Cores 100% da logo (preto + azul #0047BB→#00A6FF)
- [x] Header com equalizador
- [x] `app/api/noticias/route.ts` limpo e sem duplicatas
- [x] MundoMusicaSection voltando a listar
- [x] Fonte sem link externo
- [x] Favicon pack equalizador
- [x] README + .env.example

© 2026 Itapecuru Baladas - Itapecuru-Mirim, MA
