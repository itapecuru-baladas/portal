"use client"
import { useEffect, useState } from "react"
import { supabase } from "@/lib/supabase"

export default function MundoMusicaSection() {
  const [noticias, setNoticias] = useState<any[]>([])
  useEffect(() => {
    supabase.from("noticias_musica").select("*").order("created_at", {ascending:false}).limit(6).then(({data})=>setNoticias(data||[]))
  }, [])

  return (
    <section className="py-12 bg-zinc-950">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-black italic uppercase mb-8">MUNDO DA MÚSICA • BRASIL E MUNDO</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {noticias.length === 0 ? <p className="text-zinc-500">Carregando notícias...</p> :
          noticias.map(n=>(
            <a key={n.id} href={n.link} target="_blank" className="bg-zinc-900 rounded-xl overflow-hidden hover:scale-105 transition">
              <img src={n.imagem_url || "https://picsum.photos/400/300"} className="w-full h-48 object-cover"/>
              <div className="p-4"><span className="text-xs bg-blue-600 px-2 py-1 rounded-full">{n.categoria}</span><h3 className="font-bold mt-2 line-clamp-2">{n.titulo}</h3><p className="text-xs text-zinc-400 mt-1">{n.fonte}</p></div>
            </a>
          ))}
        </div>
      </div>
    </section>
  )
}