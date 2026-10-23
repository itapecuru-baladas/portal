"use client"
import { useEffect, useState } from "react"
import { supabase } from "@/lib/supabase"

export default function Galeria(){
  const [fotos, setFotos] = useState<any[]>([])
  const [ads, setAds] = useState<any[]>([])

  useEffect(()=>{
    async function load(){
      const { data: fotosData } = await supabase.from("fotos").select("*").order("created_at", {ascending:false}).limit(50)
      const { data: adsData } = await supabase.from("ads_spaces").select("*").eq("local","feed").eq("ativo", true)
      setFotos(fotosData||[])
      setAds(adsData||[])
    }
    load()
  },[])

  return (
    <div className="min-h-screen bg-black text-white p-4 md:p-8">
      <h1 className="text-4xl font-black mb-2">GALERIA BALADA</h1>
      <p className="text-zinc-400 mb-8">Fotos oficiais - Itapecuru Mirim</p>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {fotos.map((foto, i)=>(
          <>
            <div key={foto.id} className="group relative bg-zinc-900 rounded-xl overflow-hidden">
              {/* FOTO COM LOGO */}
              <div className="relative aspect-[4/5]">
                <img src={foto.url} className="w-full h-full object-cover" alt={foto.evento_nome}/>
                {/* Logo overlay */}
                <div className="absolute bottom- left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-3">
                  <p className="font-black text-xs tracking-widest">ITAPECURU BALADA</p>
                </div>
                {/* Barra de publicidade na foto */}
                <div className="absolute bottom-0 left-0 right-0 h- bg-black flex items-center justify-center border-t border-zinc-800">
                  <p className="text- text-zinc-500">PUBLICIDADE</p>
                </div>
              </div>

              {/* Crédito do fotógrafo */}
              <div className="p-3">
                <p className="font-bold text-sm truncate">{foto.evento_nome || "Balada"}</p>
                <p className="text-xs text-zinc-400">📸 {foto.fotografo || "Divulgação"}</p>
                {foto.whatsapp && (
                  <a href={`https://wa.me/55${foto.whatsapp.replace(/\D/g,'')}`} target="_blank" className="text- text-green-400 mt-1 inline-block">Falar com fotógrafo →</a>
                )}
              </div>
            </div>

            {/* A cada 6 fotos, injeta um banner (externo ou AdSense) */}
            {(i+1)%6===0 && ads[0] && (
              <div key={`ad-${i}`} className="col-span-2 md:col-span-1 bg-zinc-900 rounded-xl p-2 flex items-center justify-center min-h-">
                {ads[0].formato === 'adsense' ? (
                  <div dangerouslySetInnerHTML={{__html: ads[0].codigo_adsense}} />
                ) : (
                  <a href={ads[0].link} target="_blank">
                    <img src={ads[0].imagem_url} className="w-full rounded" />
                  </a>
                )}
              </div>
            )}
          </>
        ))}
      </div>
    </div>
  )
}