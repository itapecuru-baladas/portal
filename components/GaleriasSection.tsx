export default function GaleriasSection() {
  const cidades = ["Todas","Itapecuru-Mirim","Santa Rita","Rosário","Presidente Vargas"];
  const galerias = [
    { nome: "Festa do Vaqueiro 2026 - Dia 1", cidade: "Itapecuru-Mirim", fotos: 128, data: "18 OUT", img: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600" },
    { nome: "Brega Night no Arena Prime", cidade: "Itapecuru-Mirim", fotos: 86, data: "17 OUT", img: "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=600" },
    { nome: "Festival de Piseiro - Santa Rita", cidade: "Santa Rita", fotos: 210, data: "15 OUT", img: "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=600" },
    { nome: "Show de Forró na Praça", cidade: "Rosário", fotos: 54, data: "12 OUT", img: "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=600" },
  ];
  return (
    <section id="galerias" className="max-w-7xl mx-auto px-4 py-10 grid lg:grid-cols-[1fr_320px] gap-8">
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl md:text-3xl font-black italic uppercase">Galerias <span className="text-[#0A84FF]">Recentes</span></h2>
          <div className="flex gap-2 overflow-x-auto scrollbar-hide">
            {cidades.map(c=>(<button key={c} className="whitespace-nowrap text-xs font-bold uppercase px-3 py-1 rounded-full border border-white/20 hover:bg-white hover:text-black">{c}</button>))}
          </div>
        </div>
        {/* Ad inline */}
        <div className="bg-[#111] border border-dashed border-white/20 rounded-xl h-[90px] flex items-center justify-center text-[11px] text-white/40 mb-6">Espaço Anunciante - 728x90 - Patrocinado por Arena Prime</div>
        <div className="grid md:grid-cols-2 gap-4">
          {galerias.map((g,i)=>(
            <div key={i} className="relative bg-[#111] rounded-2xl overflow-hidden border border-white/10 group">
              <div className="relative h-64"><img src={g.img} className="w-full h-full object-cover" />
                <span className="absolute bottom-2 right-2 text-[9px] bg-black/70 px-2 py-1 rounded-full border border-white/20 font-bold">ITAPECURU BALADAS</span>
                <span className="absolute top-3 left-3 bg-gradient-to-r from-[#0A84FF] to-[#0066FF] text-xs font-black px-2 py-1 rounded-full">{g.fotos} FOTOS</span>
              </div>
              <div className="p-4">
                <p className="text-[10px] text-[#0A84FF] font-bold uppercase">{g.cidade} • {g.data} • Fotos por: Studio Flash</p>
                <h3 className="font-black uppercase leading-tight mt-1">{g.nome}</h3>
                <p className="text-[11px] text-white/40 mt-1">Patrocínio: Bar do Zé</p>
              </div>
            </div>
          ))}
        </div>
      </div>
      <aside className="space-y-4">
        <div className="bg-[#111] border border-dashed border-white/20 rounded-xl h-[250px] flex flex-col items-center justify-center text-xs text-white/40 sticky top-24"><span className="bg-[#0A84FF] text-white text-[10px] px-2 py-0.5 rounded mb-2">ANÚNCIO</span>300x250<br/>Seu Anúncio Aqui</div>
        <div className="bg-[#111] border border-dashed border-white/20 rounded-xl h-[400px] flex flex-col items-center justify-center text-xs text-white/40"><span className="bg-[#0A84FF] text-white text-[10px] px-2 py-0.5 rounded mb-2">ANÚNCIO</span>300x600<br/>Patrocinador Premium</div>
        <div className="bg-[#0A0A0A] border border-white/10 rounded-2xl p-4">
          <h4 className="font-black uppercase text-sm mb-3">No <span className="text-[#0A84FF]">Instagram</span></h4>
          <div className="grid grid-cols-3 gap-2">
            {[1,2,3,4,5,6].map(i=>(<div key={i} className="aspect-square bg-white/10 rounded-lg overflow-hidden"><img src={`https://images.unsplash.com/photo-1516450360452-9312abbf6f7e?w=200&sig=${i}`} className="w-full h-full object-cover" /></div>))}
          </div>
          <a href="https://instagram.com" target="_blank" className="mt-3 block text-center bg-gradient-to-r from-[#0A84FF] to-[#0066FF] py-2 rounded-full text-xs font-black uppercase">Siga @itapecurubaladas</a>
        </div>
      </aside>
    </section>
  );
}
