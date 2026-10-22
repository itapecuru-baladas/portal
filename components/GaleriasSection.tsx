import { supabase } from '@/lib/supabase'

export default async function GaleriasRecentes() {
  // Busca do Supabase - agora vai aparecer o que você criou no Table Editor
  const { data: eventos, error } = await supabase
    .from('eventos')
    .select('*')
    .eq('status', 'publicado')
    .order('data_evento', { ascending: false })
    .limit(6)

  if (error) {
    console.error('Erro Supabase:', error)
    return <div>Erro ao carregar galerias: {error.message}</div>
  }

  if (!eventos || eventos.length === 0) {
    return (
      <div className="py-10 text-center text-gray-500">
        Nenhum evento publicado ainda. Crie um no Supabase Table Editor.
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {eventos.map((evento: any) => (
        <a 
          key={evento.id} 
          href={`/galeria/${evento.slug}`}
          className="group relative overflow-hidden rounded-xl bg-gray-900"
        >
          <img 
            src={evento.capa_url || 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800'} 
            alt={evento.nome}
            className="h-64 w-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent" />
          <div className="absolute bottom-0 p-4">
            <h3 className="text-white font-bold text-lg">{evento.nome}</h3>
            <p className="text-white/80 text-sm">{evento.local || evento.cidade} • {evento.data_evento || evento.data}</p>
          </div>
        </a>
      ))}
    </div>
  )
}