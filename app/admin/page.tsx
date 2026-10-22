"use client"
import { useState, useEffect } from "react"
import { supabase } from "@/lib/supabase"

export default function AdminCompleto() {
  const [tab, setTab] = useState("eventos")
  const [eventos, setEventos] = useState<any[]>([])
  const [banners, setBanners] = useState<any[]>([])
  const [configs, setConfigs] = useState<any[]>([])

  // Forms
  const [formEvento, setFormEvento] = useState({ nome: "", local: "", capa_url: "" })
  const [formBanner, setFormBanner] = useState({ titulo: "", imagem_url: "", link: "" })
  const [formConfig, setFormConfig] = useState({ chave: "", valor: "" })

  useEffect(() => { loadAll() }, [])
  async function loadAll() {
    const [ev, bn, cf] = await Promise.all([
      supabase.from("eventos").select("*").order("created_at", {ascending:false}),
      supabase.from("banners").select("*").order("created_at", {ascending:false}),
      supabase.from("site_config").select("*")
    ])
    setEventos(ev.data || []); setBanners(bn.data || []); setConfigs(cf.data || [])
  }

  async function salvarEvento() {
    const slug = formEvento.nome.toLowerCase().replace(/\s+/g, "-") + "-" + Date.now()
    await supabase.from("eventos").insert({ ...formEvento, slug, data_evento: new Date(), status: "publicado" })
    setFormEvento({nome:"", local:"", capa_url:""}); loadAll()
  }
  async function salvarBanner() {
    await supabase.from("banners").insert(formBanner)
    setFormBanner({titulo:"", imagem_url:"", link:""}); loadAll()
  }
  async function salvarConfig() {
    await supabase.from("site_config").upsert(formConfig, {onConflict: "chave"})
    setFormConfig({chave:"", valor:""}); loadAll()
  }
  async function deletar(tabela: string, id: string) {
    if(!confirm("Deletar?")) return
    await supabase.from(tabela).delete().eq("id", id); loadAll()
  }

  return (
    <div className="min-h-screen bg-black text-white p-4 md:p-8">
      <h1 className="text-2xl font-black mb-6">ADMIN @itapecurubalada</h1>
      
      <div className="flex gap-2 mb-8">
        {["eventos","banners","redes"].map(t=>(
          <button key={t} onClick={()=>setTab(t)} className={`px-4 py-2 rounded font-bold ${tab===t?'bg-white text-black':'bg-zinc-800'}`}>{t.toUpperCase()}</button>
        ))}
      </div>

      {tab==="eventos" && (
        <>
          <div className="bg-zinc-900 p-6 rounded-xl mb-8 max-w-xl">
            <h3 className="font-bold mb-3">+ Novo Evento / Galeria</h3>
            <input placeholder="Nome - Ex: Arena Prime" value={formEvento.nome} onChange={e=>setFormEvento({...formEvento, nome:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800" />
            <input placeholder="Local" value={formEvento.local} onChange={e=>setFormEvento({...formEvento, local:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800" />
            <input placeholder="Link da Capa (https://...)" value={formEvento.capa_url} onChange={e=>setFormEvento({...formEvento, capa_url:e.target.value})} className="w-full p-3 bg-black rounded mb-3 border border-zinc-800" />
            <button onClick={salvarEvento} className="bg-white text-black px-6 py-2 rounded font-bold w-full">Salvar Evento</button>
          </div>
          {eventos.map(ev=>(
            <div key={ev.id} className="bg-zinc-900 p-4 rounded flex justify-between mb-2"><span>{ev.nome} - {ev.local}</span><button onClick={()=>deletar("eventos", ev.id)} className="text-red-500">X</button></div>
          ))}
        </>
      )}

      {tab==="banners" && (
        <>
          <div className="bg-zinc-900 p-6 rounded-xl mb-8 max-w-xl">
            <h3 className="font-bold mb-3">+ Novo Banner Home</h3>
            <input placeholder="Título" value={formBanner.titulo} onChange={e=>setFormBanner({...formBanner, titulo:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800" />
            <input placeholder="Link da Imagem (1920x600)" value={formBanner.imagem_url} onChange={e=>setFormBanner({...formBanner, imagem_url:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800" />
            <input placeholder="Link ao clicar (opcional)" value={formBanner.link} onChange={e=>setFormBanner({...formBanner, link:e.target.value})} className="w-full p-3 bg-black rounded mb-3 border border-zinc-800" />
            <button onClick={salvarBanner} className="bg-white text-black px-6 py-2 rounded font-bold w-full">Salvar Banner</button>
          </div>
          {banners.map(b=>(
            <div key={b.id} className="bg-zinc-900 p-4 rounded flex justify-between mb-2"><span>{b.titulo}</span><button onClick={()=>deletar("banners", b.id)} className="text-red-500">X</button></div>
          ))}
        </>
      )}

      {tab==="redes" && (
        <>
          <div className="bg-zinc-900 p-6 rounded-xl mb-8 max-w-xl">
            <h3 className="font-bold mb-3">+ Link / Rede Social</h3>
            <select value={formConfig.chave} onChange={e=>setFormConfig({...formConfig, chave:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800">
              <option value="">Escolha...</option>
              <option value="instagram">Instagram</option>
              <option value="whatsapp">WhatsApp</option>
              <option value="tiktok">TikTok</option>
              <option value="youtube">YouTube</option>
              <option value="facebook">Facebook</option>
            </select>
            <input placeholder="https://..." value={formConfig.valor} onChange={e=>setFormConfig({...formConfig, valor:e.target.value})} className="w-full p-3 bg-black rounded mb-3 border border-zinc-800" />
            <button onClick={salvarConfig} className="bg-white text-black px-6 py-2 rounded font-bold w-full">Salvar Link</button>
          </div>
          {configs.map(c=>(
            <div key={c.id} className="bg-zinc-900 p-4 rounded flex justify-between mb-2"><span><b>{c.chave}:</b> {c.valor}</span><button onClick={()=>deletar("site_config", c.id)} className="text-red-500">X</button></div>
          ))}
        </>
      )}
    </div>
  )
}