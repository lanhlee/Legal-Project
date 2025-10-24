import Parser from 'rss-parser'

export default async function NewsPage() {
  const parser = new Parser()
  const sources = [
    {name: 'VnExpress - Pháp luật', url: 'https://vnexpress.net/rss/phap-luat.rss'},
    {name: 'BBC World', url: 'http://feeds.bbci.co.uk/news/world/rss.xml'}
  ]

  const results = []
  for (const s of sources) {
    try {
      const feed = await parser.parseURL(s.url)
      results.push({source: s.name, items: feed.items.slice(0,6)})
    } catch (e) {
      results.push({source: s.name, items: [], error: (e as Error).message})
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Cập nhật pháp luật</h2>
      {results.map((r: any, idx:number) => (
        <div key={idx} className="mb-6">
          <h3 className="font-bold">{r.source}</h3>
          {r.error && <p className="text-red-600">Lỗi: {r.error}</p>}
          <ul className="list-disc pl-5 mt-2">
            {r.items.map((it:any,i:number)=>(
              <li key={i}>
                <a className="text-sky-600" href={it.link} target="_blank" rel="noreferrer">{it.title}</a>
                <div className="text-sm text-slate-500">{it.pubDate ?? ''}</div>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}
