"use client";
import Image from 'next/image';
import Link from 'next/link';
export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-black border-b border-white/10">
      <div className="bg-gradient-to-r from-[#0A84FF] to-[#0066FF] text-white text-[11px] py-1 px-4 flex justify-between">
        <span className="flex items-center gap-2"><span className="w-2 h-2 bg-white rounded-full animate-pulse"></span> AO VIVO - COBERTURAS EM ITAPECURU</span>
        <span className="hidden md:flex gap-3">
          <a href="#" className="hover:underline">Instagram</a><a href="#" className="hover:underline">TikTok</a><a href="#" className="hover:underline">YouTube</a>
        </span>
      </div>
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="flex items-center">
          <img src="/Logo_futurista_Itapecuru_Baladas.png" alt="Itapecuru Baladas" className="h-12 md:h-14 w-auto" />
        </Link>
        <nav className="hidden md:flex gap-6 text-sm font-bold uppercase tracking-wide">
          <Link href="/" className="hover:text-[#0A84FF]">Início</Link>
          <Link href="#flyers" className="hover:text-[#0A84FF]">Agenda da Semana</Link>
          <Link href="#musica" className="hover:text-[#0A84FF]">Mundo da Música</Link>
          <Link href="galerias" className="hover:text-[#0A84FF]">Galerias</Link>
        </nav>
        <div className="flex items-center gap-3">
          <div className="hidden md:flex gap-2">
            <a href="https://instagram.com/itapecurubalada" target="_blank" className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center hover:bg-[#0A84FF]">IG</a>
            <a href="https://tiktok.com" target="_blank" className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center hover:bg-[#0A84FF]">TT</a>
            <a href="https://youtube.com" target="_blank" className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center hover:bg-[#0A84FF]">YT</a>
          </div>
          
        </div>
      </div>
    </header>
  );
}
