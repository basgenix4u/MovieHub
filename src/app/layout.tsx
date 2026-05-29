import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MovieHub | Discover Cinema",
  description: "High-end movie discovery and aggregation platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-black text-white antialiased">
        {children}
      </body>
    </html>
  );
}
