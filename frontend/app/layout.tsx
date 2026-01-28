import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Financial Analyst",
  description: "AI-powered financial analysis dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
