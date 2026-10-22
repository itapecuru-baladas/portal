'use client'
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'

export default function GaleriasRecentes() {
  const [eventos, setEventos] = useState<any[]>([])

  useEffect(() => {
    supabase.from('eventos').select('*').eq('status','publicado').order('created_at', {ascending:false}).then(({data}) => {
      if(data) setEventos(data)
    })
  }, [])

  if(eventos.length === 0) return <div className="py-10 text-center">Carregando...</div>

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {eventos.map((evento: any) => (
        <a key={evento.id} href={`/galeria/${evento.slug}`} className="group relative overflow-hidden rounded-xl bg-gray-900">
          <img src={evento.capa_url} alt={evento.nome} className="h-64 w-full object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent" />
          <div className="absolute bottom-0 p-4">
            <h3 className="text-white font-bold">{evento.nome}</h3>
            <p className="text-white/80 text-sm">{evento.local}</p>
          </div>
        </a>
      ))}
    </div>
  )
}