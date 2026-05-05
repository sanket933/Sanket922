import './globals.css'

export const metadata = { title: 'AI Company OS', description: 'Autonomous AI company operating system' }

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>
}
