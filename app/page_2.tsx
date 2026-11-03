import MundoMusicaSection from "@/components/MundoMusicaSection";
import BannerPrincipal from "@/components/BannerPrincipal";
import BaladasSection from "@/components/BaladasSection";
import GaleriaSection from "@/components/GaleriaSection";
import FooterContatos from "@/components/FooterContatos";

export const dynamic = 'force-dynamic'

export default function Home() {
  return (
    <main className="min-h-screen bg-zinc-950">
      <header className="sticky top-0 z-50 backdrop-blur-md bg-zinc-950/80 border-b border-zinc-800">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl md:text-2xl font-black italic tracking-tighter">ITAPECURU <span className="text-zinc-500">BALADAS</span></h1>
          <nav className="hidden md:flex gap-6 text-xs uppercase tracking-widest text-zinc-400">
            <a href="#banner" className="hover:text-white">Início</a>
            <a href="#baladas" className="hover:text-white">Baladas</a>
            <a href="#galeria" className="hover:text-white">Galeria</a>
            <a href="#musica" className="hover:text-white">Música</a>
          </nav>
          <a href="/admin" className="text-xs bg-white text-black px-4 py-2 rounded-full font-bold">Admin</a>
        </div>
      </header>

      <BannerPrincipal />
      <BaladasSection />
      <GaleriaSection />
      <MundoMusicaSection />
      <FooterContatos />
    </main>
  )
}
