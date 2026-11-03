import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Itapecuru Baladas - Portal",
  description: "O maior portal de baladas e música de Itapecuru-Mirim",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="antialiased bg-zinc-950 text-zinc-100">{children}</body>
    </html>
  );
}
