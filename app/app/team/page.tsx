import fs from 'fs'
import path from 'path'
import Image from 'next/image'

export default function TeamPage() {
  const file = path.join(process.cwd(), 'data', 'team.json')
  const data = JSON.parse(fs.readFileSync(file, 'utf-8'))
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Đội ngũ chuyên gia</h2>
      <div className="grid md:grid-cols-2 gap-4">
        {data.map((m: any, idx: number) => (
          <div key={idx} className="bg-white p-4 rounded shadow">
            <h3 className="font-bold text-lg">{m.name}</h3>
            <p className="text-sky-600">{m.title}</p>
            <p className="text-slate-700 mt-2">{m.bio}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
