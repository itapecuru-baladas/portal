"use client";
import { useState, useEffect } from 'react';

type Noticia = {
  id: string;
  titulo: string;
  resumo?: string;
  categoria: string;
  link: string;
  imagem_url?: string;
  fonte?: string;
  created_at?: string;
};

const CATEGORIAS = ["TODOS","SERTANEJO","FORRÓ","PISEIRO","POP","ELETRÔNICO","BREGA","PAGODE"];

export default function MundoMusicaSection() {
  const [noticias, setNoticias] = useState<Noticia[]>([]);
  const [filtro, setFiltro] = useState("TODOS");
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const res = await fetch('/api/noticias', { cache: 'no-store' });
        const json = await res.json();
        if (!res.ok) throw new Error(json.error || 'Erro buscar noticias');
        // se for debug {data: [...]}, pega data
        const arr = Array.isArray(json) ? json : json.data || [];
        // deduplica por link
        const uniq = Array.from(new Map(arr.map((n:any)=>[n.link, n])).values());
        setNoticias(uniq);
      } catch (e:any) {
        setErro(e.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const filtradas = filtro === "TODOS" ? noticias : noticias.filter(n => n.categoria?.toUpperCase() === filtro);

  return (
    <section className="bg-[#111] text-white py-10 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
          <div>
            <h2 className="text-4xl font-black italic">MUNDO DA <span className="text-[#008CFF]">MÚSICA</span></h2>
            <p className="text-zinc-400 text-sm mt-1">Fique por dentro de tudo que rola - de forró a eletrônico</p>
          </div>
          <div className="flex flex-wrap gap-2">
            {CATEGORIAS.map(cat => (
              <button key={cat} onClick={()=>setFiltro(cat)} className={`px-4 py-1.5 rounded-full text-xs font-bold border ${filtro===cat ? 'bg-[#008CFF] border-[#008CFF] text-white' : 'border-zinc-700 text-zinc-400 hover:border-white'}`}>{cat}</button>
            ))}
          </div>
        </div>

        {loading && <p className="text-center text-zinc-500 py-20">Carregando notícias...</p>}
        {erro && <p className="text-center text-red-400 py-20">Erro: {erro} - Verifique /api/noticias</p>}
        {!loading && !erro && filtradas.length === 0 && <p className="text-center text-zinc-500 py-20">Nenhuma notícia ainda. O bot vai buscar em breve. (Total no banco: {noticias.length})</p>}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtradas.map(n => (
            <a key={n.id} href={n.link} target="_blank" className="bg-[#1a1a1a] rounded-xl overflow-hidden hover:scale-[1.02] transition">
              {n.imagem_url && <img src={n.imagem_url} alt={n.titulo} className="w-full h-48 object-cover"/>}
              <div className="p-4">
                <span className="text-[10px] bg-[#008CFF] px-2 py-1 rounded font-bold">{n.categoria}</span>
                <h3 className="font-bold mt-2 line-clamp-2">{n.titulo}</h3>
                {n.resumo && <p className="text-xs text-zinc-400 mt-1 line-clamp-2">{n.resumo}</p>}
                <p className="text-[10px] text-zinc-500 mt-2">{n.fonte}</p>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}