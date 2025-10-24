import fs from 'fs'
import path from 'path'
export default function ServicesPage() {
  const file = path.join(process.cwd(), 'data', 'services.json')
  const services = JSON.parse(fs.readFileSync(file, 'utf-8'))
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Dịch vụ</h2>
      <div className="grid md:grid-cols-2 gap-4">
        {services.map((s: any, i: number) => (
          <div key={i} className="bg-white p-4 rounded shadow">
            <h3 className="font-bold text-lg">{s.title}</h3>
            <p className="text-slate-700 mt-2">{s.desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
