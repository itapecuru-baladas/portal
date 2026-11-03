"use client"
import { useEffect, useState } from "react"

type Noticia = {
  id: string
  titulo: string
  resumo: string
  imagem_url: string
  fonte_nome: string
  created_at: string
}

export default function MundoMusicaSection() {
  const [noticias, setNoticias] = useState<Noticia[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selecionada, setSelecionada] = useState<Noticia | null>(null)

  async function load() {
    try {
      setLoading(true)
      const res = await fetch('/api/noticias', { cache: 'no-store' })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Erro ao carregar')
      setNoticias(Array.isArray(data) ? data : [])
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  return (
    <>
      <section id="musica" className="py-12 bg-zinc-950 border-t border-zinc-800">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between items-end mb-8">
            <h2 className="text-3xl md:text-4xl font-black italic uppercase tracking-tighter">
              MUNDO DA MÚSICA <span className="text-zinc-600 not-italic font-normal text-xl">• BRASIL E MUNDO</span>
            </h2>
            <button onClick={load} className="text-xs text-zinc-500 hover:text-white border border-zinc-800 px-3 py-1 rounded-full">Atualizar</button>
          </div>

          {loading && <p className="text-zinc-500 animate-pulse">Carregando notícias...</p>}
          {error && <p className="text-red-400 bg-red-950/30 border border-red-900 p-4 rounded-xl">Erro ao carregar notícias. Tente novamente.</p>}
          {!loading && !error && noticias.length === 0 && <p className="text-zinc-500">Nenhuma notícia disponível no momento.</p>}

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {noticias.map((n) => (
              <article key={n.id} onClick={() => setSelecionada(n)} className="group bg-zinc-900 rounded-[20px] overflow-hidden border border-zinc-800 hover:border-zinc-600 transition-all duration-300 hover:scale-[1.02] cursor-pointer">
                <div className="relative overflow-hidden">
                  <img src={n.imagem_url && n.imagem_url !== 'None' ? n.imagem_url : 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800'} alt={n.titulo} className="w-full h-52 object-cover group-hover:scale-105 transition duration-500" />
                  <div className="absolute top-3 left-3">
                    <span className="text-[10px] tracking-widest bg-white text-black px-2.5 py-1 rounded-full font-black uppercase">{n.fonte_nome}</span>
                  </div>
                </div>
                <div className="p-5 flex flex-col h-[200px]">
                  <h3 className="font-bold text-[17px] leading-[1.2] line-clamp-2">{n.titulo}</h3>
                  <p className="text-[13px] text-zinc-400 mt-2 line-clamp-3 flex-1">{n.resumo}</p>
                  <div className="mt-4 pt-3 border-t border-zinc-800 flex justify-between items-center">
                    <p className="text-[11px] text-zinc-500">Fonte: {n.fonte_nome}</p>
                    <p className="text-[10px] text-zinc-600">{new Date(n.created_at).toLocaleDateString('pt-BR')}</p>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {selecionada && (
        <div className="fixed inset-0 z-[100] bg-black/80 backdrop-blur flex items-center justify-center p-4" onClick={() => setSelecionada(null)}>
          <div className="bg-zinc-900 border border-zinc-800 rounded-[24px] max-w-lg w-full overflow-hidden" onClick={e => e.stopPropagation()}>
            <img src={selecionada.imagem_url && selecionada.imagem_url !== 'None' ? selecionada.imagem_url : 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800'} className="w-full h-64 object-cover" />
            <div className="p-6">
              <span className="text-[10px] bg-white text-black px-2 py-1 rounded-full font-black uppercase">{selecionada.fonte_nome}</span>
              <h3 className="text-xl font-black uppercase mt-3 leading-tight">{selecionada.titulo}</h3>
              <p className="text-sm text-zinc-300 mt-3">{selecionada.resumo}</p>
              <p className="text-[11px] text-zinc-500 mt-4 border-t border-zinc-800 pt-3">Fonte: {selecionada.fonte_nome}</p>
              <button onClick={() => setSelecionada(null)} className="mt-6 w-full bg-white text-black py-3 rounded-full font-black uppercase text-sm">Fechar</button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
