export default function FooterContatos() {
  return (
    <footer id="contato" className="bg-black border-t border-zinc-800 pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-10">
          <div className="md:col-span-2">
            <h3 className="text-3xl font-black italic tracking-tighter">ITAPECURU <span className="text-zinc-600">BALADAS</span></h3>
            <p className="text-zinc-400 mt-4 max-w-md">O maior portal de entretenimento de Itapecuru-Mirim e região. Cobertura de baladas, shows, cultura e mundo da música. Atualizado 24h.</p>
            <div className="flex gap-3 mt-6">
              <a href="https://instagram.com/eudeszinho" target="_blank" className="bg-zinc-900 border border-zinc-800 px-4 py-2 rounded-full text-xs uppercase tracking-widest hover:bg-white hover:text-black transition">Instagram</a>
              <a href="https://wa.me/5598985000000" target="_blank" className="bg-zinc-900 border border-zinc-800 px-4 py-2 rounded-full text-xs uppercase tracking-widest hover:bg-white hover:text-black transition">WhatsApp</a>
            </div>
          </div>

          <div>
            <h4 className="text-xs uppercase tracking-[0.2em] text-zinc-500 font-bold mb-4">Navegação</h4>
            <ul className="space-y-2 text-sm text-zinc-300">
              <li><a href="#baladas" className="hover:text-white">Agenda de Baladas</a></li>
              <li><a href="#galeria" className="hover:text-white">Galeria de Fotos</a></li>
              <li><a href="#musica" className="hover:text-white">Mundo da Música</a></li>
              <li><a href="/admin" className="hover:text-white">Área Admin</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs uppercase tracking-[0.2em] text-zinc-500 font-bold mb-4">Contato</h4>
            <ul className="space-y-2 text-sm text-zinc-300">
              <li>Itapecuru-Mirim • MA</li>
              <li>contato@itapecurubaladas.com.br</li>
              <li>(98) 9 8500-0000</li>
              <li className="pt-2 text-[11px] text-zinc-500">Fonte das notícias: G1, Rolling Stone, etc. Sem link externo, apenas citação.</li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-zinc-900 flex flex-col md:flex-row justify-between gap-4 text-[11px] text-zinc-600 uppercase tracking-widest">
          <p>© 2026 Itapecuru Baladas. Todos os direitos reservados.</p>
          <p>Portal Limpo v2.0 • API /api/noticias</p>
        </div>
      </div>
    </footer>
  )
}
