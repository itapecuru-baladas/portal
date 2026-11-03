import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Itapecuru Baladas | Registrando momentos, conectando pessoas.",
  description: "Portal oficial de baladas, festas e música de Itapecuru-Mirim",
  icons: { icon: "/logo.png" }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="bg-black text-white antialiased">{children}</body>
    </html>
  );
}
