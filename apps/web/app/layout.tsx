import './globals.css'
import Link from 'next/link'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="container">
          <h1>TFit</h1>
          <nav style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
            <Link href="/">Home</Link>
            <Link href="/onboarding">Onboarding</Link>
            <Link href="/today">Today</Link>
            <Link href="/coach">Coach</Link>
          </nav>
          {children}
        </div>
      </body>
    </html>
  )
}
