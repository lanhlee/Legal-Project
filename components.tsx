import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-white shadow">
      <div className="container mx-auto flex items-center justify-between px-4 py-4">
        <Link href="/" className="text-xl font-bold text-slate-900">LegalPortal</Link>
        <nav className="space-x-4">
          <Link href="/about" className="text-slate-700 hover:text-slate-900">Giới thiệu</Link>
          <Link href="/team" className="text-slate-700 hover:text-slate-900">Đội ngũ</Link>
          <Link href="/services" className="text-slate-700 hover:text-slate-900">Dịch vụ</Link>
          <Link href="/news" className="text-slate-700 hover:text-slate-900">Cập nhật</Link>
          <Link href="/contact" className="text-slate-700 hover:text-slate-900">Liên hệ</Link>
        </nav>
      </div>
    </header>
  );
}
