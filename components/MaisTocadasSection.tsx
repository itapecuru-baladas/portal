"use client"
import { useEffect, useState } from "react"

type Musica = {
  posicao: number
  titulo: string
  artista: string
  capa_url: string
  spotify_url: string
  youtube_url: string
  fonte: string
  plays?: string
}

export default function MaisTocadasSection() {
  const [musicas, setMusicas] = useState<Musica[]>([])
  const [filtro, setFiltro] = useState<'todas' | 'spotify' | 'youtube'>('todas')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/top', { cache: 'no-store' })
      .then(r => r.json())
      .then(data => {
        setMusicas(Array.isArray(data) ? data : [])
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const filtradas = musicas.filter(m => filtro === 'todas' ? true : m.fonte === filtro)

  return (
    <section id="musica" className="py-16 bg-zinc-950 border-t border-zinc-800">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
          <div>
            <h2 className="text-3xl md:text-5xl font-black italic uppercase tracking-tighter leading-none">
              MAIS<br/>TOCADAS<br/><span className="text-zinc-600 not-italic font-normal text-2xl">• BRASIL</span>
            </h2>
            <p className="text-zinc-400 text-sm mt-3">Top Spotify e YouTube atualizado diariamente</p>
          </div>

          <div className="flex gap-2">
            <button onClick={() => setFiltro('todas')} className={`px-5 py-2 rounded-full text-xs font-black uppercase tracking-wide border transition ${filtro==='todas' ? 'bg-white text-black border-white' : 'border-zinc-700 text-zinc-400 hover:text-white'}`}>Todas</button>
            <button onClick={() => setFiltro('spotify')} className={`px-5 py-2 rounded-full text-xs font-black uppercase tracking-wide border transition ${filtro==='spotify' ? 'bg-green-500 text-black border-green-500' : 'border-zinc-700 text-zinc-400 hover:text-white'}`}>Spotify</button>
            <button onClick={() => setFiltro('youtube')} className={`px-5 py-2 rounded-full text-xs font-black uppercase tracking-wide border transition ${filtro==='youtube' ? 'bg-red-600 text-white border-red-600' : 'border-zinc-700 text-zinc-400 hover:text-white'}`}>YouTube</button>
          </div>
        </div>

        {loading ? <p className="text-zinc-500 animate-pulse">Carregando hits...</p> : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtradas.map(m => (
              <div key={`${m.fonte}-${m.posicao}`} className="group bg-zinc-900 rounded-[20px] border border-zinc-800 p-4 flex gap-4 hover:border-zinc-600 transition">
                <div className="relative">
                  <span className="absolute -top-2 -left-2 w-6 h-6 bg-white text-black rounded-full text-[11px] font-black flex items-center justify-center z-10">{m.posicao}</span>
                  <img src={m.capa_url || 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300'} alt={m.titulo} className="w-20 h-20 rounded-xl object-cover" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-bold text-[15px] leading-tight truncate">{m.titulo}</h3>
                  <p className="text-xs text-zinc-400 truncate mt-1">{m.artista}</p>
                  <div className="flex gap-2 mt-3">
                    {m.spotify_url && <a href={m.spotify_url} target="_blank" className="text-[10px] bg-green-500 text-black px-3 py-1 rounded-full font-bold uppercase hover:scale-105 transition">Spotify</a>}
                    {m.youtube_url && <a href={m.youtube_url} target="_blank" className="text-[10px] bg-red-600 text-white px-3 py-1 rounded-full font-bold uppercase hover:scale-105 transition">YouTube</a>}
                    {!m.spotify_url && !m.youtube_url && <span className="text-[10px] border border-zinc-700 text-zinc-500 px-3 py-1 rounded-full uppercase">Em alta</span>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}
