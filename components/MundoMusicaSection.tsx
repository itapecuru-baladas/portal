"use client"
import { useEffect, useState } from "react"
import { supabase } from "@/lib/supabase"

export default function MundoMusicaSection() {
  const [noticias, setNoticias] = useState<any[]>([])
  useEffect(() => {
    supabase.from("noticias_musica").select("*").order("created_at",{ascending:false}).limit(6).then(({data})=>setNoticias(data||[]))
  }, [])
  return (
    <section className="py-12 bg-zinc-950">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-black italic uppercase mb-8">MUNDO DA MÚSICA • BRASIL E MUNDO</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {noticias.length===0 ? <p className="text-zinc-500">Carregando...</p> :
          noticias.map((n:any)=>{
            const linkReal = n.conteudo_original || n.link
            const resumoLimpo = n.resumo?.split("Via:")[0] || ""
            return (
              <a key={n.id} href={linkReal} target="_blank" className="bg-zinc-900 rounded-xl overflow-hidden hover:scale-105 transition block">
                <img src={n.imagem_url || "https://picsum.photos/400/300"} className="w-full h-48 object-cover"/>
                <div className="p-4">
                  <span className="text-xs bg-blue-600 px-2 py-1 rounded-full uppercase">{n.fonte || "G1"}</span>
                  <h3 className="font-bold mt-2 line-clamp-2">{n.titulo}</h3>
                  <p className="text-sm text-zinc-400 mt-2 line-clamp-3">{resumoLimpo}</p>
                  <p className="text-xs text-zinc-500 mt-2">Via: {n.fonte}</p>
                </div>
              </a>
            )
          })}
        </div>
      </div>
    </section>
  )
}