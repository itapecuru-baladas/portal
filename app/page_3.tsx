import MundoMusicaSection from "@/components/MundoMusicaSection";

export const dynamic = 'force-dynamic'

export default function Home() {
 return (
  <main className="min-h-screen bg-zinc-950">
   <header className="border-b border-zinc-800 py-6">
    <div className="max-w-7xl mx-auto px-4 flex justify-between items-center">
     <h1 className="text-2xl font-black italic tracking-tighter">ITAPECURU <span className="text-zinc-500">BALADAS</span></h1>
     <span className="text-xs bg-green-500 text-black px-3 py-1 rounded-full font-bold">PORTAL LIMPO v2.0</span>
    </div>
   </header>
   
   <section className="max-w-7xl mx-auto px-4 py-16">
    <h2 className="text-5xl font-black uppercase leading-none">Seu portal<br/>de música<br/><span className="text-zinc-600">e balada.</span></h2>
   </section>

   <MundoMusicaSection />

   <footer className="py-10 text-center text-zinc-600 text-xs border-t border-zinc-900 mt-10">
    Itapecuru Baladas • Portal Limpo • API /api/noticias
   </footer>
  </main>
 )
}
