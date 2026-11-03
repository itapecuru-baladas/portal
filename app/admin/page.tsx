"use client"
export default function AdminPage() {
  return (
    <main className="min-h-screen bg-zinc-950 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <a href="/" className="text-xs border border-zinc-800 px-4 py-2 rounded-full">← Voltar</a>
        <h1 className="text-4xl font-black uppercase mt-8">Admin • Itapecuru Baladas</h1>
        <p className="text-zinc-400 mt-2">Área administrativa para gerenciamento de conteúdo.</p>
        <div className="mt-8 p-4 bg-zinc-900 border border-zinc-800 rounded-xl text-sm text-zinc-300">
          Portal v2.0 • Sistema atualizado • Conteúdo dinâmico
        </div>
      </div>
    </main>
  )
}
