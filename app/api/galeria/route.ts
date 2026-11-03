import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'
export const dynamic = 'force-dynamic'
export async function GET() {
  try {
    const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!)
    const { data } = await supabase.from('galeria').select('*').order('created_at', { ascending: false }).limit(12)
    if (data && data.length > 0) return NextResponse.json(data.map((f:any)=>({id:f.id, url:f.imagem_url||f.url, titulo:f.titulo})), { headers: { 'Cache-Control': 'no-store' } })
  } catch {}
  return NextResponse.json([], { headers: { 'Cache-Control': 'no-store' } })
}
