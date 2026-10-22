'use client'
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import Link from 'next/link'

export default function GaleriasSection() {
  const [eventos, setEventos] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const { data, error } = await supabase
        .from('eventos')
        .select('*')
        .eq('status', 'publicado')
        .order('created_at', { ascending: false })
        .limit(9)
      
      console.log('Supabase data:', data, 'error:', error)
      if (data) setEventos(data)
      setLoading(false)
    }
    load()
  }, [])

  if (loading) {
    return (
      <section className="max-w-7xl mx-auto px-4 py-10">
        <h2 className="text-2xl font-black uppercase italic mb-6">Galerias Recentes</h2>
        <div className="text-white/50">Carregando galerias...</div>
      </section>
    )
  }

  return (
    <section className="max-w-7xl mx-auto px-4 py-10">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-black uppercase italic">Galerias Recentes</h2>
        <span className="text-xs text-white/50">{eventos.length} eventos</span>
      </div>

      {eventos.length === 0 ? (
        <div className="bg-white/5 border border-dashed border-white/10 rounded-xl p-10 text-center">
          <p className="text-white/70">Nenhum evento encontrado.</p>
          <p className="text-xs text-white/40 mt-2">Verifique no Supabase se status = publicado</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {eventos.map((evento) => (
            <Link 
              key={evento.id} 
              href={`/galeria/${evento.slug}`}
              className="group relative overflow-hidden rounded-xl bg-[#111] border border-white/5 hover:border-[#0A84FF]/50 transition"
            >
              <img 
                src={evento.capa_url || 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800'} 
                alt={evento.nome}
                className="h-64 w-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent" />
              <div className="absolute bottom-0 p-4 w-full">
                <span className="text-[10px] font-black uppercase bg-[#0A84FF] px-2 py-1 rounded-full">{evento.cidade}</span>
                <h3 className="text-white font-black uppercase italic text-lg leading-none mt-2">{evento.nome}</h3>
                <p className="text-white/60 text-xs mt-1">{evento.local} • {evento.data_evento ? new Date(evento.data_evento).toLocaleDateString('pt-BR') : ''}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </section>
  )
}