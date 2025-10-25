import { useEffect, useMemo, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import manifest from '../data/books.manifest.json'

export default function Reader() {
  const { id } = useParams()
  const book = useMemo(() => manifest.find(b => b.id === id), [id])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [stats, setStats] = useState({ chars: 0, words: 0 })

  useEffect(() => {
    let cancelled = false
    async function load() {
      if (!book) { setLoading(false); return }
      try {
        const res = await fetch(book.textPath)
        if (!res.ok) throw new Error(`No se pudo cargar el texto (${res.status})`)
        const txt = await res.text()
        if (cancelled) return
        const chars = txt.length
        const words = txt.trim().split(/\s+/).length
        setStats({ chars, words })
      } catch (e) {
        setError(e.message || 'Error cargando el texto')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [book])

  if (!book) {
    return (
      <main style={{ padding: 24 }}>
        <p>No se encontró el libro solicitado.</p>
        <Link to="/">Volver</Link>
      </main>
    )
  }

  return (
    <main className="readerShell">
      <div className="readerHeader">
        <div className="readerCover" style={{ backgroundImage: `url(${book.coverPath})` }} />
        <div className="readerMeta">
          <h1>{book.title}</h1>
          <p style={{ opacity: 0.8 }}>{book.author}</p>
          <p style={{ opacity: 0.7, marginTop: 6 }}>
            {loading ? 'Cargando...' : error ? `Error: ${error}` : `~${stats.words.toLocaleString()} palabras • ${stats.chars.toLocaleString()} caracteres`}
          </p>
          <div style={{ marginTop: 12 }}>
            <a href={book.textPath} target="_blank" rel="noreferrer" className="introCta">Ver texto crudo</a>{' '}
            <Link to="/" className="introCta" style={{ background: '#2a3257', color: '#e7e9ee' }}>Volver</Link>
          </div>
        </div>
      </div>

      {/* Placeholder del lector: aquí luego montamos paginación y búsqueda */}
      <section className="readerStage">
        <div className="stagePlaceholder">
          <p>El e-reader se implementará aquí en los siguientes pasos: paginación, búsqueda exacta, y autocompletado.</p>
        </div>
      </section>
    </main>
  )
}
