"use client"
export default function BannerPrincipal() {
  return (
    <section id="banner" className="relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600 via-pink-600 to-orange-500 opacity-90"></div>
      <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=1600')] bg-cover bg-center mix-blend-overlay"></div>
      <div className="absolute inset-0 bg-gradient-to-t from-zinc-950 via-zinc-950/50 to-transparent"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 py-20 md:py-32">
        <div className="max-w-3xl">
          <span className="inline-block text-[11px] tracking-[0.2em] bg-white text-black px-3 py-1 rounded-full font-black uppercase mb-6">ITAPECURU-MIRIM • MA</span>
          <h2 className="text-5xl md:text-7xl font-black uppercase leading-[0.9] tracking-tighter">
            A NOITE<br/>É NOSSA.<br/><span className="text-zinc-300">O PORTAL<br/>É SEU.</span>
          </h2>
          <p className="text-zinc-300 mt-6 text-lg max-w-xl">Os melhores eventos, baladas, shows e o mundo da música em um só lugar.</p>
          <div className="flex gap-3 mt-8">
            <a href="#baladas" className="bg-white text-black px-6 py-3 rounded-full font-black uppercase text-sm tracking-wide hover:scale-105 transition">Ver Agenda</a>
            <a href="#musica" className="border border-white/30 text-white px-6 py-3 rounded-full font-bold uppercase text-sm tracking-wide hover:bg-white hover:text-black transition">Mundo da Música</a>
          </div>
        </div>
      </div>
    </section>
  )
}
