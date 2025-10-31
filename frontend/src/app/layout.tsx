import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "../context/AuthContext";

export const metadata: Metadata = {
  title: "Interview Buddy",
  description: "Run Soal Labs interviews with clarity and consistency"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <div className="app-shell">
            <header className="app-header">
              <h1>Interview Buddy</h1>
              <span className="muted">Soal Labs internal</span>
            </header>
            <main className="app-main">{children}</main>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
