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

  async function load() {
    try {
      setLoading(true)
      const res = await fetch('/api/noticias', { cache: 'no-store' })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Erro ao buscar noticias')
      setNoticias(Array.isArray(data) ? data : [])
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  return (
    <section className="py-12 bg-zinc-950 border-t border-zinc-800">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-end mb-8">
          <h2 className="text-3xl md:text-4xl font-black italic uppercase tracking-tighter">
            MUNDO DA MÚSICA <span className="text-zinc-600 not-italic font-normal text-xl">• BRASIL E MUNDO</span>
          </h2>
          <button onClick={load} className="text-xs text-zinc-500 hover:text-white border border-zinc-800 px-3 py-1 rounded-full">Atualizar</button>
        </div>

        {loading && <p className="text-zinc-500 animate-pulse">Carregando notícias...</p>}
        {error && <p className="text-red-400 bg-red-950/30 border border-red-900 p-4 rounded-xl">Erro: {error} - Verifique /api/noticias</p>}

        {!loading && !error && noticias.length === 0 && (
          <p className="text-zinc-500">Nenhuma notícia no banco. Rode seu bot /forcar-noticias</p>
        )}

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {noticias.map((n) => (
            <article key={n.id} className="group bg-zinc-900 rounded-[20px] overflow-hidden border border-zinc-800 hover:border-zinc-600 transition-all duration-300 hover:scale-[1.02]">
              <div className="relative overflow-hidden">
                <img src={n.imagem_url} alt={n.titulo} className="w-full h-52 object-cover group-hover:scale-105 transition duration-500" />
                <div className="absolute top-3 left-3">
                  <span className="text-[10px] tracking-widest bg-white text-black px-2.5 py-1 rounded-full font-black uppercase">
                    {n.fonte_nome}
                  </span>
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
  )
}
