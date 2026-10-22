"use client"
import { useEffect, useState } from "react"
import { supabase } from "@/lib/supabase"
import Link from "next/link"

export default function EventosProximos() {
  const [eventos, setEventos] = useState<any[]>([])
  useEffect(() => {
    async function load() {
      const hoje = new Date().toISOString().split('T')[0]
      const { data } = await supabase.from("eventos").select("*").gte("data_evento", hoje).eq("status", "publicado").order("data_evento", { ascending: true }).limit(6)
      setEventos(data || [])
    }
    load()
  }, [])
  if (eventos.length === 0) return null
  return (
    <section className="py-12 bg-black">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-black italic uppercase mb-8">EVENTOS PRÓXIMOS</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {eventos.map(ev => (
            <Link key={ev.id} href={`/evento/${ev.slug}`} className="group">
              <div className="bg-zinc-900 rounded-xl overflow-hidden">
                <img src={ev.capa_url} alt={ev.nome} className="w-full h-56 object-cover group-hover:scale-105 transition" />
                <div className="p-4">
                  <p className="text-xs text-zinc-400">{new Date(ev.data_evento).toLocaleDateString('pt-BR')}</p>
                  <h3 className="font-bold">{ev.nome}</h3>
                  <p className="text-xs text-zinc-500">{ev.local}</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
}