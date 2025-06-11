import './globals.css'

export const metadata = {
  title: 'Attendance Management System',
  description: 'Laboratory attendance management system',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-100 min-h-screen">{children}</body>
    </html>
  )
}
