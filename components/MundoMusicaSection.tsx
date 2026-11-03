"use client";
import { useEffect, useState } from "react";

type Noticia = {
  id: string;
  titulo: string;
  resumo: string;
  categoria?: string;
  capa_url?: string;
  created_at: string;
  fonte?: string;
};

export default function MundoMusicaSection() {
  const [noticias, setNoticias] = useState<Noticia[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("/api/noticias", { cache: "no-store" });
        const data = await res.json();
        if (Array.isArray(data)) setNoticias(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <section id="mundo-musica" className="max-w-7xl mx-auto px-6 py-12">
      <div className="flex items-end gap-4 mb-8">
        <h3 className="futur-title text-white text-xl md:text-2xl tracking-widest">MUNDO DA MÚSICA</h3>
        <div className="flex gap-1 mb-1.5">
          {[8,12,18,24,32,24,18,12,8].map((h,i)=>(
            <div key={i} className="ib-equalizer-bar w-[4px]" style={{height: h}} />
          ))}
        </div>
        <div className="h-[1px] flex-1 bg-gradient-to-r from-[#0077FF] to-transparent ml-4 mb-3" />
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1,2,3,4,5,6].map(i=>(
            <div key={i} className="h-64 bg-white/[0.04] animate-pulse rounded-lg border border-white/5" />
          ))}
        </div>
      ) : noticias.length === 0 ? (
        <p className="text-white/40 text-sm">Nenhuma notícia encontrada no Supabase.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {noticias.map(n => (
            <article key={n.id || n.titulo} className="group bg-[#0A0A0A] border border-white/10 rounded-xl overflow-hidden hover:border-[#0077FF]/50 transition">
              {n.capa_url && <div className="h-44 w-full bg-cover bg-center" style={{backgroundImage: `url(${n.capa_url})`}} />}
              <div className="p-5">
                <span className="futur-title text-[10px] tracking-widest text-[#00A6FF]">{n.categoria || "MÚSICA"}</span>
                <h4 className="mt-2 font-bold text-white leading-tight group-hover:text-[#00A6FF] transition line-clamp-2">{n.titulo}</h4>
                <p className="mt-2 text-sm text-white/60 line-clamp-2">{n.resumo}</p>
                <div className="mt-4 flex justify-between items-center">
                  <span className="text-[11px] text-white/30">{new Date(n.created_at).toLocaleDateString("pt-BR")}</span>
                  {/* CITAÇÃO DA FONTE SEM LINK EXTERNO - padrão Itapecuru Baladas */}
                  <span className="text-[11px] tracking-widest text-white/40 font-light">Fonte: Itapecuru Baladas</span>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
