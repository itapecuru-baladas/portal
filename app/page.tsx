import Header from "@/components/Header";
import MundoMusicaSection from "@/components/MundoMusicaSection";
import Hero from "@/components/Hero";

export default function Page() {
  return (
    <main className="min-h-screen bg-black">
      <Header />
      <Hero />
      <MundoMusicaSection />
      <footer className="border-t border-white/10 py-8 mt-16">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-white/60 text-sm tracking-[0.2em] font-light">Registrando momentos, conectando pessoas.</p>
          <p className="text-white/30 text-xs">© {new Date().getFullYear()} Itapecuru Baladas • Itapecuru-Mirim, MA</p>
        </div>
      </footer>
    </main>
  );
}
