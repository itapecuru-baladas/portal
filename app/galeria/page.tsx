import GaleriaSection from "@/components/GaleriaSection"
export default function GaleriaPage() {
 return (
  <main className="bg-zinc-950 min-h-screen">
   <div className="max-w-7xl mx-auto px-4 py-6">
    <a href="/" className="text-xs border border-zinc-800 px-4 py-2 rounded-full text-white">← Voltar pra Home</a>
   </div>
   <GaleriaSection />
  </main>
 )
}
