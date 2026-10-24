"use client";
import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';

type Noticia = {
  id: string;
  titulo: string;
  resumo: string;
  link: string;
  imagem_url: string;
  fonte: string;
  created_at: string;
};

export default function MundoMusicaSection() {
  const cats = ["Todos","Sertanejo","Forró","Piseiro","Pop","Eletrônico","Brega","Pagode"];
  const [active, setActive] = useState("Todos");
  const [noticias, setNoticias] = useState<Noticia[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchNoticias() {
      const { data, error } = await supabase
        .from("noticias_musica")
        .select("*")
        .order("created_at", { ascending: false })
        .limit(12);
      if (error) {
        console.error("Erro buscar noticias_musica:", error);
      } else if (data) {
        setNoticias(data as Noticia[]);
      }
      setLoading(false);
    }
    fetchNoticias();
  }, []);

  if (loading) {
    return (
      <section id="musica" className="bg-[#0A0A0A] py-10 border-y border-white/5">
        <div className="max-w-7xl mx-auto px-4 text-white/50">Carregando notícias...</div>
      </section>
    );
  }

  return (
    <section id="musica" className="bg-[#0A0A0A] py-10 border-y border-white/5">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
          <div>
            <h2 className="text-3xl md:text-4xl font-black italic uppercase">Mundo da <span className="text-[#0A84FF]">Música</span></h2>
            <p className="text-white/60 text-sm mt-1">Fique por dentro de tudo que rola - de forró a eletrônico, de piseiro a pop</p>
          </div>
          <div className="flex gap-2 overflow-x-auto scrollbar-hide">
            {cats.map(c=>(
              <button key={c} onClick={()=>setActive(c)} className={`whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold uppercase border ${active===c ? 'bg-gradient-to-r from-[#0A84FF] to-[#0066FF] border-[#0A84FF] text-white' : 'border-white/20 text-white/60 hover:border-white/40'}`}>{c}</button>
            ))}
          </div>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          {noticias.map((n,i)=>(
            <a key={n.id || i} href={n.link} target="_blank" rel="noopener noreferrer" className="bg-[#111] rounded-2xl overflow-hidden border border-white/10 group cursor-pointer hover:border-[#0A84FF]/40 block">
              <div className="relative h-44">
                <img src={n.imagem_url || "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600"} className="w-full h-full object-cover group-hover:scale-105 transition duration-500" alt={n.titulo} />
                <span className="absolute top-3 left-3 bg-black/70 backdrop-blur text- font-black px-2 py-1 rounded-full border border-white/20">{(n.fonte || "G1").toUpperCase()}</span>
              </div>
              <div className="p-4">
                <p className="text- text-white/50 mb-2">{new Date(n.created_at).toLocaleDateString('pt-BR')}</p>
                <h3 className="font-bold leading-tight line-clamp-2 text-white">{n.titulo}</h3>
                <p className="text-xs text-white/50 mt-2 line-clamp-2">{n.resumo}</p>
              </div>
            </a>
          ))}
        </div>
        {noticias.length === 0 && (
          <p className="text-white/50 text-center py-10">Nenhuma notícia ainda. Verifique o bot em itapecuru-bot.onrender.com/forcar-noticias</p>
        )}
      </div>
    </section>
  );
}