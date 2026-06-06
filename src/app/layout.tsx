import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { AuthProvider } from '@/context/AuthContext';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-black text-white antialiased`}>
        <AuthProvider>
          <Navbar />
          <div className="min-h-screen">
            {children}
          </div>
          <Footer />
        </AuthProvider>
      </body>
    </html>
  );
}
