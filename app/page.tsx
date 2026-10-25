import MundoMusicaSection from '../components/MundoMusicaSection'
export default function Home() {
  return (
    <main>
      <div className="p-6 text-center">
        <h1 className="text-2xl font-bold">Itapecuru Baladas - Portal</h1>
        <p className="text-zinc-400 text-sm mt-2">Deploy limpo funcionando</p>
        <a href="/api/noticias" target="_blank" className="text-[#008CFF] text-xs underline mt-2 inline-block">Testar /api/noticias</a>
      </div>
      <MundoMusicaSection />
    </main>
  )
}