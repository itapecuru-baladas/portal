import "./globals.css";
export const metadata = { title: "Itapecuru Baladas - Registrando momentos, conectando pessoas", description: "Cobertura de eventos, flyers, galerias e notícias do mundo da música de Itapecuru-Mirim e região" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="pt-BR"><body>{children}</body></html>;
}
