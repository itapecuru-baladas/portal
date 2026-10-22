import Header from '@/components/Header';
import FlyersSection from '@/components/FlyersSection';
import MundoMusicaSection from '@/components/MundoMusicaSection';
import GaleriasSection from '@/components/GaleriasSection';

export const dynamic = 'force-dynamic'
export const revalidate = 0

export default function Home() {
  return (
    <main className="min-h-screen bg-black">
      <Header />
      {/* Hero */}
      <section className="relative h-[60vh] md:h-[70vh] overflow-hidden">
        <img src="https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=1600" className="absolute inset-0 w-full h-full object-cover" alt="" />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-transparent"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-black/80 to-transparent"></div>
        <div className="relative max-w-7xl mx-auto px-4 h-full flex items-end pb-10">
          <div className="max-w-2xl">
            <span className="inline-flex items-center gap-2 bg-gradient-to-r from-[#0A84FF] to-[#0066FF] text-white text-xs font-black px-3 py-1 rounded-full uppercase">Destaque • Itapecuru-Mirim</span>
            <h1 className="text-4xl md:text-6xl font-black italic uppercase leading-[0.9] mt-3">Festa do Vaqueiro 2026<br/><span className="text-[#0A84FF]">120 Fotos Exclusivas</span></h1>
            <p className="text-white/70 mt-3 text-sm md:text-base">Registrando momentos, conectando pessoas. Cobertura completa da maior festa da região.</p>
            <button className="mt-6 bg-white text-black font-black uppercase px-6 py-3 rounded-full text-sm hover:bg-[#0A84FF] hover:text-white transition">Ver Galeria Completa</button>
          </div>
        </div>
        {/* Ad Top */}
        <div className="absolute top-4 right-4 hidden lg:flex bg-white/10 backdrop-blur border border-dashed border-white/20 rounded-lg h-[90px] w-[728px] items-center justify-center text-xs text-white/50">Espaço Anunciante - Leaderboard 728x90</div>
      </section>

      <FlyersSection />
      <MundoMusicaSection />
      <GaleriasSection />

      {/* Footer */}
      <footer className="bg-[#0A0A0A] border-t border-white/10 py-10 mt-10">
        <div className="max-w-7xl mx-auto px-4 grid md:grid-cols-3 gap-8">
          <div><img src="/Logo_futurista_Itapecuru_Baladas.png" className="h-14 w-auto" alt="" /><p className="text-white/60 text-sm mt-3">Registrando momentos, conectando pessoas.<br/>Cobertura de eventos de Itapecuru-Mirim e região.</p></div>
          <div><h4 className="font-black uppercase text-sm mb-3">Cidades</h4><ul className="text-sm text-white/60 space-y-1"><li>Itapecuru-Mirim</li><li>Santa Rita</li><li>Rosário</li><li>Presidente Vargas</li></ul></div>
          <div><h4 className="font-black uppercase text-sm mb-3">Siga @itapecurubaladas</h4><div className="flex gap-2"><a className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-[#0A84FF]">IG</a><a className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-[#0A84FF]">TT</a><a className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-[#0A84FF]">YT</a><a className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-[#0A84FF]">WA</a></div><p className="text-xs text-white/40 mt-4">© 2026 Itapecuru Baladas. Todos os direitos reservados.</p></div>
        </div>
      </footer>
    </main>
  );
}