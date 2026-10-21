export default function FlyersSection() {
  const flyers = [
    { id: 1, titulo: "Brega Night - Ed. Especial", cidade: "Itapecuru-Mirim", data: "25 OUT", local: "Arena Prime", img: "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400" },
    { id: 2, titulo: "Festival de Piseiro", cidade: "Santa Rita", data: "26 OUT", local: "Parque do Povo", img: "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400" },
    { id: 3, titulo: "Noite do Sertanejo", cidade: "Rosário", data: "27 OUT", local: "Clube do Vaqueiro", img: "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=400" },
    { id: 4, titulo: "Baile do Balada", cidade: "Itapecuru-Mirim", data: "28 OUT", local: "Estação", img: "https://images.unsplash.com/photo-1516450360452-9312abbf6f7e?w=400" },
  ];
  return (
    <section id="flyers" className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl md:text-3xl font-black italic uppercase tracking-tighter">Agenda da <span className="text-[#0A84FF]">Semana</span></h2>
        <span className="text-xs bg-white/10 px-3 py-1 rounded-full">FLYERS OFICIAIS</span>
      </div>
      <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2">
        {flyers.map(f => (
          <div key={f.id} className="min-w-[260px] bg-[#111] rounded-2xl overflow-hidden border border-white/10 hover:border-[#0A84FF]/50 transition">
            <div className="relative h-72">
              <img src={f.img} className="w-full h-full object-cover" />
              <div className="absolute top-3 left-3 bg-gradient-to-r from-[#0A84FF] to-[#0066FF] text-white text-xs font-black px-2 py-1 rounded">{f.data}</div>
              <div className="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black to-transparent">
                <p className="text-[10px] text-[#0A84FF] font-bold uppercase">{f.cidade} • {f.local}</p>
                <p className="font-black text-sm uppercase leading-tight">{f.titulo}</p>
              </div>
            </div>
            <div className="p-3"><button className="w-full bg-white text-black text-xs font-black py-2 rounded-full uppercase">Ver Evento</button></div>
          </div>
        ))}
      </div>
    </section>
  );
}
