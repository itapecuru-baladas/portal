"use client"
import { useEffect, useState } from "react"

type Balada = {
 id: string
 nome: string
 local: string
 data: string
 imagem_url: string
 destaque?: boolean
}

const FALLBACK_BALADAS: Balada[] = [
 { id: '1', nome: 'Sexta do Piseiro', local: 'Arena Itapecuru', data: 'Sexta • 22h', imagem_url: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800', destaque: true },
 { id: '2', nome: 'Pagode do Marinho', local: 'Bar do Cais', data: 'Sábado • 20h', imagem_url: 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=800' },
 { id: '3', nome: 'Eletrônica Sunset', local: 'Ranchos Park', data: 'Domingo • 17h', imagem_url: 'https://images.unsplash.com/photo-1516450360452-9312abbf6f7e?w=800' },
]

export default function BaladasSection() {
 const [baladas, setBaladas] = useState<Balada[]>(FALLBACK_BALADAS)

 useEffect(() => {
  fetch('/api/baladas', { cache: 'no-store' })
  .then(r => r.json())
  .then(data => {
    if (Array.isArray(data) && data.length > 0) setBaladas(data)
   })
  .catch(() => {})
 }, [])

 return (
  <section id="baladas" className="py-16 bg-zinc-950 border-t border-zinc-900">
   <div className="max-w-7xl mx-auto px-4">
    <div className="flex justify-between items-end mb-8">
     <h2 className="text-3xl md:text-4xl font-black italic uppercase tracking-tighter">PRÓXIMAS<br/>BALADAS</h2>
     <a href="/galeria" className="text-xs text-zinc-500 hover:text-white uppercase tracking-widest border border-zinc-800 px-4 py-2 rounded-full">Ver todas</a>
    </div>

    <div className="grid md:grid-cols-3 gap-6">
     {baladas.map(b => (
      <div key={b.id} className="group relative rounded-[24px] overflow-hidden bg-zinc-900 border border-zinc-800 h-[380px]">
       <img src={b.imagem_url} className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition duration-700" />
       <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent"></div>
       {b.destaque && <span className="absolute top-4 left-4 bg-yellow-400 text-black text-[10px] font-black px-3 py-1 rounded-full uppercase">Destaque</span>}
       <div className="absolute tom-0 p-6 w-full">
        <p className="text-[11px] tracking-widest text-zinc-300 uppercase">{b.data} • {b.local}</p>
        <h3 className="text-2xl font-black uppercase leading-none mt-2">{b.nome}</h3>
        <button className="mt-4 bg-white text-black text-xs font-black px-4 py-2 rounded-full uppercase">Garantir Mesa</button>
       </div>
      </div>
     ))}
    </div>
   </div>
  </section>
 )
}
