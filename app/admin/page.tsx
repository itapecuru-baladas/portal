"use client";
import { useState } from 'react';
export default function Admin() {
  const [auth, setAuth] = useState(false);
  const [pwd, setPwd] = useState("");
  const check = () => { if(pwd==="itapecuru2026") setAuth(true); else alert("Senha errada"); };
  if(!auth) return <div className="min-h-screen bg-black flex items-center justify-center p-4"><div className="bg-[#111] p-6 rounded-2xl w-full max-w-sm border border-white/10"><h2 className="font-black uppercase mb-4">Admin - Itapecuru Baladas</h2><input value={pwd} onChange={e=>setPwd(e.target.value)} placeholder="Senha" type="password" className="w-full bg-black border border-white/20 rounded-full px-4 py-2 text-sm" /><button onClick={check} className="mt-3 w-full bg-[#0A84FF] py-2 rounded-full font-black uppercase text-sm">Entrar</button><p className="text-xs text-white/40 mt-2">Senha padrão: itapecuru2026 (troque no .env)</p></div></div>;
  return <div className="min-h-screen bg-black text-white p-6"><h1 className="text-2xl font-black uppercase">Painel de Aprovação</h1><p className="text-white/60 text-sm mt-2">Aqui lista os eventos com status rascunho do Supabase. Conecte o supabase client para listar e aprovar.</p><div className="mt-6 bg-[#111] border border-dashed border-white/20 rounded-xl h-64 flex items-center justify-center text-white/40">Lista de galerias pendentes - integrar com supabase.from('eventos').select()</div></div>;
}
