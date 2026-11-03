import Image from "next/image";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-black/95 backdrop-blur border-b border-white/10">
      <div className="max-w-7xl mx-auto px-6 h-[72px] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <img src="/logo.png" alt="Itapecuru Baladas" className="h-10 w-auto" />
        </div>
        <nav className="hidden md:flex items-center gap-8">
          <a className="futur-title text-[12px] tracking-widest text-white/80 hover:text-white transition" href="#mundo-musica">MUNDO DA MÚSICA</a>
          <a className="futur-title text-[12px] tracking-widest text-white/80 hover:text-white transition" href="#">BALADAS</a>
          <a className="futur-title text-[12px] tracking-widest text-white/80 hover:text-white transition" href="#">CONTATO</a>
        </nav>
        <div className="flex items-center gap-1">
          {[6,10,14,18,22,18,14,10,6].map((h,i)=>(
            <div key={i} className="ib-equalizer-bar w-[5px]" style={{height: h}} />
          ))}
        </div>
      </div>
      <div className="ib-swoosh w-full" />
    </header>
  );
}
