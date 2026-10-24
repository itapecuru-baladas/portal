import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY! // <- tem que adicionar essa key na Vercel
);

export async function GET() {
  const { data, error } = await supabase
    .from('noticias_musica')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(12);

  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json(data);
}