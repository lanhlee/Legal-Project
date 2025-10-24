export default function Footer(){
  return (
    <footer className="bg-slate-900 text-white mt-12">
      <div className="container mx-auto px-4 py-6 text-center">
        © {new Date().getFullYear()} LegalPortal • Email: info@example.com • Hotline: 0123-456-789
      </div>
    </footer>
  )
}
