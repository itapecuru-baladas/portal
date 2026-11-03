import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

export const dynamic = 'force-dynamic'
export const revalidate = 0

export async function GET() {
  try {
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
    const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

    if (!supabaseUrl || !supabaseKey) {
      return NextResponse.json({ error: 'ENV vars do Supabase não configuradas na Vercel' }, { status: 500 })
    }

    const supabase = createClient(supabaseUrl, supabaseKey)

    const { data, error } = await supabase
      .from('noticias_musica')
      .select('id, titulo, resumo, imagem_url, fonte, created_at, conteudo_original')
      .order('created_at', { ascending: false })
      .limit(60)

    if (error) {
      // Retorna erro legível para debugar PGRST205 etc
      return NextResponse.json({ error: error.message, code: error.code, details: error.details }, { status: 500 })
    }

    // Deduplicação + Limpeza de resumo + Fonte sem link
    const seen = new Set<string>()
    const limpas = (data || [])
      .filter((n: any) => {
        if (!n.titulo) return false
        const key = n.titulo.toLowerCase().trim()
        if (seen.has(key)) return false
        seen.add(key)
        return true
      })
      .map((n: any) => {
        let resumoLimpo = (n.resumo || '').toString()
        // Remove sufixos que o bot antigo colocava
        resumoLimpo = resumoLimpo.split('Via:')[0]
        resumoLimpo = resumoLimpo.split('Confira')[0]
        resumoLimpo = resumoLimpo.split('Leia mais')[0]
        resumoLimpo = resumoLimpo.split('Fonte:')[0]
        resumoLimpo = resumoLimpo.trim()
        if (resumoLimpo.length > 180) resumoLimpo = resumoLimpo.slice(0, 180).trim() + '...'

        return {
          id: n.id,
          titulo: n.titulo.trim(),
          resumo: resumoLimpo,
          imagem_url: n.imagem_url,
          fonte_nome: n.fonte, // Só texto, SEM link externo
          created_at: n.created_at
        }
      })
      .slice(0, 12)

    return NextResponse.json(limpas, {
      headers: {
        'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    })
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: 500 })
  }
}
