import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'
export const revalidate = 0

// Fallback caso não tenha chaves ainda
const FALLBACK = [
  { posicao: 1, titulo: 'Barulho do Foguete', artista: 'Zé Vaqueiro', capa_url: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600', spotify_url: 'https://open.spotify.com', youtube_url: 'https://youtube.com', fonte: 'spotify', plays: '12M' },
  { id: 2, posicao: 2, titulo: 'Nosso Quadro', artista: 'Ana Castela', capa_url: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600', spotify_url: 'https://open.spotify.com', youtube_url: 'https://youtube.com', fonte: 'spotify', plays: '10M' },
  { id: 3, posicao: 3, titulo: 'Let Me Down Slowly', artista: 'Alec Benjamin', capa_url: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600', spotify_url: 'https://open.spotify.com', youtube_url: 'https://youtube.com', fonte: 'youtube', plays: '8M' },
]

async function getSpotifyToken() {
  const id = process.env.SPOTIFY_CLIENT_ID
  const secret = process.env.SPOTIFY_CLIENT_SECRET
  if (!id || !secret) return null
  try {
    const res = await fetch('https://accounts.spotify.com/api/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + Buffer.from(id + ':' + secret).toString('base64')
      },
      body: 'grant_type=client_credentials',
      cache: 'no-store'
    })
    const data = await res.json()
    return data.access_token
  } catch { return null }
}

export async function GET() {
  try {
    let musicas: any[] = []

    // 1. Tenta Spotify
    const token = await getSpotifyToken()
    if (token) {
      try {
        // Top 50 Brasil playlist oficial
        const playlistId = '37i9dQZ9XDWdP594TQEnba'
        const res = await fetch(`https://api.spotify.com/v1/playlists/${playlistId}/tracks?limit=15`, {
          headers: { Authorization: `Bearer ${token}` },
          cache: 'no-store'
        })
        const data = await res.json()
        if (data.items) {
          musicas = data.items.map((item: any, idx: number) => ({
            posicao: idx + 1,
            titulo: item.track?.name || 'Desconhecido',
            artista: item.track?.artists?.map((a: any) => a.name).join(', ') || '',
            capa_url: item.track?.album?.images?.[0]?.url || '',
            spotify_url: item.track?.external_urls?.spotify || '',
            youtube_url: '',
            fonte: 'spotify',
            plays: ''
          }))
        }
      } catch {}
    }

    // 2. Tenta YouTube (se tiver key)
    const ytKey = process.env.YOUTUBE_API_KEY
    if (ytKey && musicas.length < 10) {
      try {
        const res = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&videoCategoryId=10&regionCode=BR&maxResults=10&key=${ytKey}`, { cache: 'no-store' })
        const data = await res.json()
        if (data.items) {
          const ytMusicas = data.items.map((item: any, idx: number) => ({
            posicao: musicas.length + idx + 1,
            titulo: item.snippet?.title || '',
            artista: item.snippet?.channelTitle || '',
            capa_url: item.snippet?.thumbnails?.high?.url || '',
            spotify_url: '',
            youtube_url: `https://www.youtube.com/watch?v=${item.id}`,
            fonte: 'youtube',
            plays: item.statistics?.viewCount || ''
          }))
          musicas = [...musicas, ...ytMusicas]
        }
      } catch {}
    }

    if (musicas.length === 0) musicas = FALLBACK

    return NextResponse.json(musicas.slice(0, 15), {
      headers: { 'Cache-Control': 'no-store' }
    })
  } catch (e: any) {
    return NextResponse.json(FALLBACK, { headers: { 'Cache-Control': 'no-store' } })
  }
}
