"use client";
import { useState } from 'react';
export default function MundoMusicaSection() {
  const cats = ["Todos","Sertanejo","Forró","Piseiro","Pop","Eletrônico","Brega","Pagode"];
  const [active, setActive] = useState("Todos");
  const noticias = [
    { titulo: "João Gomes anuncia nova turnê pelo Nordeste com show em Itapecuru", cat: "Forró", tempo: "2h atrás", img: "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600" },
    { titulo: "Anitta quebra recorde no Spotify com novo single", cat: "Pop", tempo: "5h atrás", img: "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600" },
    { titulo: "Piseiro domina Top 10 do YouTube Brasil essa semana", cat: "Piseiro", tempo: "1d atrás", img: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=600" },
    { titulo: "Festival de música eletrônica confirma edição em São Luís", cat: "Eletrônico", tempo: "1d atrás", img: "https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?w=600" },
  ];
  const filtered = active==="Todos" ? noticias : noticias.filter(n=>n.cat===active);
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
          {filtered.map((n,i)=>(
            <article key={i} className="bg-[#111] rounded-2xl overflow-hidden border border-white/10 group cursor-pointer hover:border-[#0A84FF]/40">
              <div className="relative h-44"><img src={n.img} className="w-full h-full object-cover group-hover:scale-105 transition duration-500" /><span className="absolute top-3 left-3 bg-black/70 backdrop-blur text-[10px] font-black px-2 py-1 rounded-full border border-white/20">{n.cat.toUpperCase()}</span></div>
              <div className="p-4"><p className="text-[11px] text-white/50 mb-2">{n.tempo}</p><h3 className="font-bold leading-tight line-clamp-2">{n.titulo}</h3><p className="text-xs text-white/50 mt-2 line-clamp-2">Confira os detalhes dessa novidade que está movimentando o cenário musical...</p></div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
