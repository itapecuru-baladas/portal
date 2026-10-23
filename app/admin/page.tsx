"use client"
import { useState, useEffect } from "react"
import { supabase } from "@/lib/supabase"

const USER = "admin"
const PASS = "itapecuru2026" // <-- TROCA ESSA SENHA

export default function Admin() {
  const [logado, setLogado] = useState(false)
  const [login, setLogin] = useState({ user: "", pass: "" })
  const [tab, setTab] = useState("eventos")
  
  const [eventos, setEventos] = useState<any[]>([])
  const [ads, setAds] = useState<any[]>([])
  const [configs, setConfigs] = useState<any[]>([])
  
  const [formEvento, setFormEvento] = useState({ nome: "", local: "", capa_url: "" })
  const [formAd, setFormAd] = useState({ nome: "", tamanho: "728x90", local: "topo_home", imagem_url: "", link: "", ativo: true })
  const [formConfig, setFormConfig] = useState({ chave: "instagram", valor: "" })

  useEffect(() => {
    if(localStorage.getItem("admin_logado") === "true") setLogado(true)
    loadAll()
  }, [])

  async function loadAll() {
    const [ev, ad, cf] = await Promise.all([
      supabase.from("eventos").select("*").order("created_at", {ascending:false}),
      supabase.from("ads_spaces").select("*").order("created_at", {ascending:false}),
      supabase.from("site_config").select("*")
    ])
    setEventos(ev.data||[]); setAds(ad.data||[]); setConfigs(cf.data||[])
  }

  function fazerLogin() {
    if(login.user === USER && login.pass === PASS) {
      setLogado(true)
      localStorage.setItem("admin_logado", "true")
    } else alert("Usuário ou senha errados!")
  }

  async function salvarEvento() {
    const slug = formEvento.nome.toLowerCase().replace(/\s+/g, "-") + "-" + Date.now()
    await supabase.from("eventos").insert({...formEvento, slug, data_evento: new Date(), status: "publicado"})
    setFormEvento({nome:"", local:"", capa_url:""}); loadAll()
  }
  async function salvarAd() {
    await supabase.from("ads_spaces").insert(formAd)
    setFormAd({nome:"", tamanho:"728x90", local:"topo_home", imagem_url:"", link:"", ativo:true}); loadAll()
  }
  async function salvarConfig() {
    await supabase.from("site_config").upsert(formConfig, {onConflict:"chave"})
    setFormConfig({chave:"instagram", valor:""}); loadAll()
  }
  async function deletar(tabela:string, id:string) {
    if(!confirm("Deletar?")) return
    await supabase.from(tabela).delete().eq("id", id); loadAll()
  }

  if(!logado) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <div className="bg-zinc-900 p-8 rounded-xl w-full max-w-sm">
          <h1 className="text-2xl font-black mb-6">ADMIN @itapecurubalada</h1>
          <input placeholder="Usuário" value={login.user} onChange={e=>setLogin({...login, user:e.target.value})} className="w-full p-3 bg-black border border-zinc-800 rounded mb-2" />
          <input type="password" placeholder="Senha" value={login.pass} onChange={e=>setLogin({...login, pass:e.target.value})} className="w-full p-3 bg-black border border-zinc-800 rounded mb-4" />
          <button onClick={fazerLogin} className="w-full bg-white text-black font-bold py-3 rounded">Entrar</button>
          <p className="text-xs text-zinc-500 mt-4">user: admin / senha: itapecuru2026</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white p-4 md:p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-black">PAINEL - ITAPECURU BALADA</h1>
        <button onClick={()=>{localStorage.removeItem("admin_logado"); setLogado(false)}} className="text-sm bg-zinc-800 px-4 py-2 rounded">Sair</button>
      </div>
      
      <div className="flex gap-2 mb-8 flex-wrap">
        {["eventos","publicidade","redes"].map(t=>(
          <button key={t} onClick={()=>setTab(t)} className={`px-4 py-2 rounded font-bold uppercase text-sm ${tab===t?'bg-white text-black':'bg-zinc-800'}`}>{t}</button>
        ))}
      </div>

      {tab==="eventos" && (
        <>
          <div className="bg-zinc-900 p-6 rounded-xl mb-8 max-w-xl">
            <h3 className="font-bold mb-3">+ Novo Evento</h3>
            <input placeholder="Nome da Festa" value={formEvento.nome} onChange={e=>setFormEvento({...formEvento, nome:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800" />
            <input placeholder="Local" value={formEvento.local} onChange={e=>setFormEvento({...formEvento, local:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800" />
            <input placeholder="Link da Capa" value={formEvento.capa_url} onChange={e=>setFormEvento({...formEvento, capa_url:e.target.value})} className="w-full p-3 bg-black rounded mb-3 border border-zinc-800" />
            <button onClick={salvarEvento} className="bg-white text-black px-6 py-2 rounded font-bold w-full">Salvar Evento</button>
          </div>
          {eventos.map(ev=>(<div key={ev.id} className="bg-zinc-900 p-4 rounded flex justify-between mb-2"><span>{ev.nome}</span><button onClick={()=>deletar("eventos", ev.id)} className="text-red-500">X</button></div>))}
        </>
      )}

      {tab==="publicidade" && (
        <>
          <div className="bg-zinc-900 p-6 rounded-xl mb-8 max-w-xl">
            <h3 className="font-bold mb-3">+ Novo Anúncio / Banner</h3>
            <input placeholder="Nome do anunciante - Ex: Arena Prime" value={formAd.nome} onChange={e=>setFormAd({...formAd, nome:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800" />
            <div className="flex gap-2 mb-2">
              <select value={formAd.tamanho} onChange={e=>setFormAd({...formAd, tamanho:e.target.value})} className="w-1/2 p-3 bg-black rounded border border-zinc-800"><option>728x90</option><option>300x250</option><option>970x90</option><option>300x600</option></select>
              <select value={formAd.local} onChange={e=>setFormAd({...formAd, local:e.target.value})} className="w-1/2 p-3 bg-black rounded border border-zinc-800"><option value="topo_home">Topo Home</option><option value="sidebar">Sidebar</option><option value="meio_feed">Meio do Feed</option><option value="rodape">Rodapé</option></select>
            </div>
            <input placeholder="Link da Imagem do Banner" value={formAd.imagem_url} onChange={e=>setFormAd({...formAd, imagem_url:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800" />
            <input placeholder="Link ao clicar" value={formAd.link} onChange={e=>setFormAd({...formAd, link:e.target.value})} className="w-full p-3 bg-black rounded mb-3 border border-zinc-800" />
            <button onClick={salvarAd} className="bg-white text-black px-6 py-2 rounded font-bold w-full">Salvar Publicidade</button>
          </div>
          {ads.map(a=>(
            <div key={a.id} className="bg-zinc-900 p-4 rounded flex justify-between items-center mb-2">
              <div><p className="font-bold">{a.nome} - {a.tamanho}</p><p className="text-xs text-zinc-400">{a.local} - {a.ativo?'ATIVO':'INATIVO'}</p></div>
              <button onClick={()=>deletar("ads_spaces", a.id)} className="text-red-500">X</button>
            </div>
          ))}
        </>
      )}

      {tab==="redes" && (
        <>
          <div className="bg-zinc-900 p-6 rounded-xl mb-8 max-w-xl">
            <h3 className="font-bold mb-3">Links / Redes Sociais</h3>
            <select value={formConfig.chave} onChange={e=>setFormConfig({...formConfig, chave:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800">
              <option value="instagram">Instagram @itapecurubalada</option><option value="whatsapp">WhatsApp</option><option value="tiktok">TikTok</option><option value="youtube">YouTube</option>
            </select>
            <input placeholder="https://..." value={formConfig.valor} onChange={e=>setFormConfig({...formConfig, valor:e.target.value})} className="w-full p-3 bg-black rounded mb-3 border border-zinc-800" />
            <button onClick={salvarConfig} className="bg-white text-black px-6 py-2 rounded font-bold w-full">Salvar Link</button>
          </div>
          {configs.map(c=>(<div key={c.id} className="bg-zinc-900 p-4 rounded flex justify-between mb-2"><span><b>{c.chave}:</b> {c.valor}</span><button onClick={()=>deletar("site_config", c.id)} className="text-red-500">X</button></div>))}
        </>
      )}
    </div>
  )
}