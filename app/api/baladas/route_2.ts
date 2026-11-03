import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'
export const dynamic = 'force-dynamic'
export async function GET() {
 try {
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!)
  const { data } = await supabase.from('baladas').select('*').order('data_evento', { ascending: true }).limit(10)
  if (data && data.length > 0) return NextResponse.json(data, { headers: { 'Cache-Control': 'no-store' } })
 } catch {}
 // Se não tiver tabela, retorna vazio e front usa fallback
 return NextResponse.json([], { headers: { 'Cache-Control': 'no-store' } })
}
