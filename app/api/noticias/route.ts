import { createClient } from "@supabase/supabase-js";
import { NextResponse } from "next/server";

// Evita cache na Vercel - sempre busca do Supabase
export const dynamic = "force-dynamic";
export const revalidate = 0;

export async function GET() {
  try {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
    const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
    
    if (!url || !key) {
      return NextResponse.json({ error: "Supabase env faltando" }, { status: 500 });
    }

    const supabase = createClient(url, key);

    // TABELA UNICA: noticias - corrige duplicatas
    const { data, error } = await supabase
      .from("noticias")
      .select("id, titulo, resumo, categoria, capa_url, created_at, fonte")
      .order("created_at", { ascending: false })
      .limit(30);

    if (error) throw error;

    // Remove duplicatas por id/titulo se houver
    const unique = Array.from(new Map((data || []).map((n: any) => [n.titulo, n])).values());

    return NextResponse.json(unique, {
      headers: { "Cache-Control": "no-store" }
    });

  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: 500 });
  }
}
