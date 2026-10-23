"use client"
import { useState, useEffect } from "react"
import { supabase } from "@/lib/supabase"

const USER = "admin"
const PASS = "itapecuru2026"

export default function Admin() {
  const [logado, setLogado] = useState(false)
  const [login, setLogin] = useState({ user: "", pass: "" })
  const [tab, setTab] = useState("eventos")
  const [eventos, setEventos] = useState<any[]>([])
  const [ads, setAds] = useState<any[]>([])
  const [noticias, setNoticias] = useState<any[]>([])
  const [charts, setCharts] = useState<any[]>([])

  const [formEvento, setFormEvento] = useState({ nome: "", local: "", capa_url: "" })
  const [formAd, setFormAd] = useState({ nome: "", tamanho: "728x90", local: "topo_home", imagem_url: "", link: "" })
  const [formNoticia, setFormNoticia] = useState({ titulo: "", link: "", fonte: "" })

  useEffect(() => {
    if(localStorage.getItem("admin_logado")==="true") setLogado(true)
    loadAll()
  }, [])

  async function loadAll() {
    const [ev, ad, nt, ch] = await Promise.all([
      supabase.from("eventos").select("*").order("created_at",{ascending:false}),
      supabase.from("ads_spaces").select("*").order("created_at",{ascending:false}),
      supabase.from("noticias_musica").select("*").order("created_at",{ascending:false}).limit(20),
      supabase.from("charts_musica").select("*").order("posicao")
    ])
    setEventos(ev.data||[]); setAds(ad.data||[]); setNoticias(nt.data||[]); setCharts(ch.data||[])
  }

  function fazerLogin() {
    if(login.user===USER && login.pass===PASS){ setLogado(true); localStorage.setItem("admin_logado","true") }
    else alert("Senha errada!")
  }

  async function salvar(tabela:string, dados:any, setForm:any) {
    await supabase.from(tabela).insert(dados)
    setForm({}); loadAll()
  }
  async function deletar(tabela:string, id:string){ if(confirm("Deletar?")){ await supabase.from(tabela).delete().eq("id",id); loadAll() } }

  if(!logado) return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <div className="bg-zinc-900 p-8 rounded-xl w-full max-w-sm">
        <h1 className="text-2xl font-black mb-6">ADMIN</h1>
        <input placeholder="Usuário" value={login.user} onChange={e=>setLogin({...login,user:e.target.value})} className="w-full p-3 bg-black border border-zinc-800 rounded mb-2"/>
        <input type="password" placeholder="Senha" value={login.pass} onChange={e=>setLogin({...login,pass:e.target.value})} className="w-full p-3 bg-black border border-zinc-800 rounded mb-4"/>
        <button onClick={fazerLogin} className="w-full bg-white text-black font-bold py-3 rounded">Entrar</button>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-black text-white p-4 md:p-8">
      <div className="flex justify-between mb-6"><h1 className="text-2xl font-black">PAINEL ITAPECURU BALADA</h1><button onClick={()=>{localStorage.removeItem("admin_logado"); setLogado(false)}} className="bg-zinc-800 px-4 py-2 rounded text-sm">Sair</button></div>
      
      <div className="flex gap-2 mb-8 flex-wrap">
        {[
          {id:"eventos", label:"Eventos"},
          {id:"publicidade", label:"Publicidade"},
          {id:"noticias", label:"Mundo da Música"},
          {id:"charts", label:"Mais Tocadas (Bot)"}
        ].map(t=>(
          <button key={t.id} onClick={()=>setTab(t.id)} className={`px-4 py-2 rounded font-bold uppercase text-sm ${tab===t.id?'bg-white text-black':'bg-zinc-800'}`}>{t.label}</button>
        ))}
      </div>

      {tab==="eventos" && (
        <div>
          <div className="bg-zinc-900 p-6 rounded-xl mb-6 max-w-xl">
            <h3 className="font-bold mb-3">+ Novo Evento</h3>
            <input placeholder="Nome" value={formEvento.nome} onChange={e=>setFormEvento({...formEvento,nome:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800"/>
            <input placeholder="Local" value={formEvento.local} onChange={e=>setFormEvento({...formEvento,local:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800"/>
            <input placeholder="Capa URL" value={formEvento.capa_url} onChange={e=>setFormEvento({...formEvento,capa_url:e.target.value})} className="w-full p-3 bg-black rounded mb-3 border border-zinc-800"/>
            <button onClick={()=>{ const slug=formEvento.nome.toLowerCase().replace(/\s+/g,"-")+"-"+Date.now(); supabase.from("eventos").insert({...formEvento,slug,data_evento:new Date(),status:"publicado"}).then(()=>{setFormEvento({nome:"",local:"",capa_url:""}); loadAll()}) }} className="bg-white text-black px-6 py-2 rounded font-bold w-full">Salvar</button>
          </div>
          {eventos.map(ev=><div key={ev.id} className="bg-zinc-900 p-4 rounded flex justify-between mb-2">{ev.nome}<button onClick={()=>deletar("eventos",ev.id)} className="text-red-500">X</button></div>)}
        </div>
      )}

      {tab==="publicidade" && (
        <div>
          <div className="bg-zinc-900 p-6 rounded-xl mb-6 max-w-xl">
            <h3 className="font-bold mb-3">+ Novo Banner</h3>
            <input placeholder="Anunciante" value={formAd.nome} onChange={e=>setFormAd({...formAd,nome:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800"/>
            <input placeholder="Imagem Banner" value={formAd.imagem_url} onChange={e=>setFormAd({...formAd,imagem_url:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800"/>
            <input placeholder="Link" value={formAd.link} onChange={e=>setFormAd({...formAd,link:e.target.value})} className="w-full p-3 bg-black rounded mb-3 border border-zinc-800"/>
            <button onClick={()=>salvar("ads_spaces",formAd,setFormAd)} className="bg-white text-black px-6 py-2 rounded font-bold w-full">Salvar Banner</button>
          </div>
          {ads.map(a=><div key={a.id} className="bg-zinc-900 p-4 rounded flex justify-between mb-2">{a.nome} - {a.tamanho}<button onClick={()=>deletar("ads_spaces",a.id)} className="text-red-500">X</button></div>)}
        </div>
      )}

      {tab==="noticias" && (
        <div>
          <div className="bg-zinc-900 p-6 rounded-xl mb-6 max-w-xl">
            <h3 className="font-bold mb-3">+ Notícia Manual (o bot também posta automático)</h3>
            <input placeholder="Título" value={formNoticia.titulo} onChange={e=>setFormNoticia({...formNoticia,titulo:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800"/>
            <input placeholder="Link" value={formNoticia.link} onChange={e=>setFormNoticia({...formNoticia,link:e.target.value})} className="w-full p-3 bg-black rounded mb-2 border border-zinc-800"/>
            <input placeholder="Fonte" value={formNoticia.fonte} onChange={e=>setFormNoticia({...formNoticia,fonte:e.target.value})} className="w-full p-3 bg-black rounded mb-3 border border-zinc-800"/>
            <button onClick={()=>salvar("noticias_musica",formNoticia,setFormNoticia)} className="bg-white text-black px-6 py-2 rounded font-bold w-full">Salvar Notícia</button>
          </div>
          <p className="text-xs text-zinc-500 mb-2">Bot posta automático a cada 3h + você pode postar manual aqui</p>
          {noticias.map(n=><div key={n.id} className="bg-zinc-900 p-4 rounded flex justify-between mb-2 text-sm">{n.titulo.slice(0,50)}<button onClick={()=>deletar("noticias_musica",n.id)} className="text-red-500 ml-2">X</button></div>)}
        </div>
      )}

      {tab==="charts" && (
        <div>
          <p className="text-sm text-zinc-400 mb-4">Atualizado automaticamente pelo bot do Render a cada 3h (【entity-Spotify¦canonical_name=Spotify】 + YouTube). Você pode apagar se quiser.</p>
          {charts.map(c=><div key={c.id} className="bg-zinc-900 p-3 rounded flex justify-between mb-2 text-sm"><span>{c.posicao}. {c.musica} - {c.artista} ({c.plataforma})</span><button onClick={()=>deletar("charts_musica",c.id)} className="text-red-500">X</button></div>)}
        </div>
      )}
    </div>
  )
}