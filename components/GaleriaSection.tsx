"use client"
import { useEffect, useState } from "react"

type Foto = { id: string; url: string; titulo: string }

const FALLBACK = [
  { id: '1', url: 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800', titulo: 'Noite de sábado' },
  { id: '2', url: 'https://images.unsplash.com/photo-1516450360452-9312abbf6f7e?w=800', titulo: 'Pista lotada' },
  { id: '3', url: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800', titulo: 'Show ao vivo' },
  { id: '4', url: 'https://images.unsplash.com/photo-1504704911898-68304a7d2807?w=800', titulo: 'Balada VIP' },
  { id: '5', url: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800', titulo: 'DJ set' },
  { id: '6', url: 'https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?w=800', titulo: 'Galera' },
]

export default function GaleriaSection() {
  const [fotos, setFotos] = useState<Foto[]>(FALLBACK)

  useEffect(() => {
    fetch('/api/galeria', { cache: 'no-store' })
      .then(r => r.json())
      .then(d => { if (Array.isArray(d) && d.length > 0) setFotos(d) })
      .catch(() => {})
  }, [])

  return (
    <section id="galeria" className="py-16 bg-zinc-900/50 border-y border-zinc-800">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-black italic uppercase tracking-tighter mb-8">GALERIA <span className="text-zinc-600 font-normal">• NOITES</span></h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {fotos.map(f => (
            <div key={f.id} className="relative aspect-[4/3] rounded-2xl overflow-hidden group bg-zinc-800">
              <img src={f.url} alt={f.titulo} className="w-full h-full object-cover group-hover:scale-110 transition duration-700" />
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition"></div>
              <p className="absolute bottom-2 left-3 text-[11px] uppercase tracking-wide opacity-0 group-hover:opacity-100 transition text-white font-bold">{f.titulo}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
