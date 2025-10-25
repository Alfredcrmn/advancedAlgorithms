// src/pages/Reader.jsx
import { useEffect, useMemo, useState, useCallback } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import Sidebar from '../components/Sidebar/Sidebar'
import Viewer from '../components/Viewer/Viewer'
import manifest from '../data/books.manifest.json'

// util super simple para paginar por tamaño aproximado de caracteres
function paginateText(text, opts = {}) {
  const targetChars = opts.targetChars ?? 1800
  const tolerance  = opts.tolerance  ?? 200

  const paras = text.replace(/\r/g, '').split(/\n{2,}/)
  const pages = []
  let buf = ''

  for (const raw of paras) {
    const p = raw.trim()
    if (!p) continue

    const candidate = buf ? buf + '\n\n' + p : p
    if (candidate.length <= targetChars + tolerance) {
      buf = candidate
      continue
    }

    if (buf) {
      pages.push(buf)
      buf = ''
    }

    if (p.length > targetChars * 1.5) {
      // partir por oraciones si el párrafo es larguísimo
      const sentences = p.split(/(?<=[.!?])\s+/)
      let temp = ''
      for (const s of sentences) {
        const cand = temp ? temp + ' ' + s : s
        if (cand.length > targetChars + tolerance) {
          if (temp) pages.push(temp.trim())
          temp = s
        } else {
          temp = cand
        }
      }
      if (temp) pages.push(temp.trim())
    } else {
      buf = p
    }
  }
  if (buf) pages.push(buf)
  return pages
}

export default function Reader() {
  const { slug } = useParams()
  const navigate = useNavigate()

  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState('')
  const [pages, setPages]     = useState([])
  const [current, setCurrent] = useState(-1) // -1 = portada
  const [showInfo, setShowInfo] = useState(false)
  const [showSearch, setShowSearch] = useState(false) // placeholder

  const bookMeta = useMemo(() => {
    if (!manifest || !Array.isArray(manifest)) return null
    return manifest.find(b => b.slug === slug) ?? null
  }, [slug])

  const base = import.meta.env.BASE_URL || '/'
  const coverUrl = `${base}books/${slug}/cover.webp`
  const bookUrl  = `${base}books/${slug}/book.txt`

  useEffect(() => {
    let active = true
    async function load() {
      try {
        setLoading(true)
        setError('')
        const res = await fetch(bookUrl)
        if (!res.ok) throw new Error('No se pudo cargar el texto')
        const txt = await res.text()
        const pgs = paginateText(txt)
        if (!active) return
        setPages(pgs)
        setCurrent(-1) // siempre iniciar en portada
      } catch (e) {
        setError(String(e.message ?? e))
      } finally {
        setLoading(false)
      }
    }
    load()
    return () => { active = false }
  }, [bookUrl])

  const onHome = useCallback(() => navigate('/'), [navigate])
  const onToggleInfo = useCallback(() => setShowInfo(v => !v), [])
  const onToggleSearch = useCallback(() => setShowSearch(v => !v), [])

  // estado de navegación
  const atCover   = current < 0
  const atLast    = pages.length > 0 && current === pages.length - 1
  const canGoPrev = !atCover
  const canGoNext = atCover || !atLast

  const goPrev = useCallback(() => {
    setCurrent(p => {
      if (p < 0) return p
      if (p === 0) return -1
      return p - 1
    })
  }, [])

  const goNext = useCallback(() => {
    setCurrent(p => {
      if (p < 0 && pages.length > 0) return 0
      if (p >= pages.length - 1) return p
      return p + 1
    })
  }, [pages.length])

  // teclas ← / →
  useEffect(() => {
    const onKey = (e) => {
      if (e.key === 'ArrowLeft')  { e.preventDefault(); if (canGoPrev) goPrev() }
      if (e.key === 'ArrowRight') { e.preventDefault(); if (canGoNext) goNext() }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [canGoPrev, canGoNext, goPrev, goNext])

  // progreso de lectura (0-100)
  const progress = useMemo(() => {
    if (current < 0 || pages.length === 0) return 0
    return Math.floor(((current + 1) / pages.length) * 100)
  }, [current, pages.length])

  return (
    <div className="reader-shell">
      <Sidebar
        onHome={onHome}
        onInfoToggle={onToggleInfo}
        onSearchToggle={onToggleSearch}
      />

      {/* TRES COLUMNAS: prev | libro | next */}
      <div className="reader-stage three-cols">
        <div
          className="nav-rail nav-rail--left"
          onClick={canGoPrev ? goPrev : undefined}
          aria-hidden={!canGoPrev}
        >
          {canGoPrev && (
            <button
              className="nav-rail__btn"
              onClick={(e)=>{e.stopPropagation(); goPrev()}}
              aria-label="Página anterior"
            >
              ‹
            </button>
          )}
        </div>

        <Viewer
          loading={loading}
          error={error}
          coverUrl={coverUrl}
          pages={pages}
          currentPage={current}
          setCurrentPage={setCurrent}
        />

        <div
          className="nav-rail nav-rail--right"
          onClick={canGoNext ? goNext : undefined}
          aria-hidden={!canGoNext}
        >
          {canGoNext && (
            <button
              className="nav-rail__btn"
              onClick={(e)=>{e.stopPropagation(); goNext()}}
              aria-label="Página siguiente"
            >
              ›
            </button>
          )}
        </div>

        {/* Panel Info del libro */}
        <aside className={`info-panel ${showInfo ? 'open' : ''}`}>
          <div className="info-panel__header">
            <h3>Book info</h3>
            <button className="btn-ghost" onClick={onToggleInfo} aria-label="Close">×</button>
          </div>

          {bookMeta ? (
            <div className="info-panel__body">
              <p><strong>Title:</strong> {bookMeta.title}</p>
              <p><strong>Author:</strong> {bookMeta.author}</p>
              {bookMeta.year && <p><strong>Year:</strong> {bookMeta.year}</p>}
              {bookMeta.language && <p><strong>Language:</strong> {bookMeta.language}</p>}
              <hr />
              <p><strong>Progress:</strong> {progress}%</p>
              <p><strong>Pages:</strong> {pages.length}</p>
            </div>
          ) : (
            <div className="info-panel__body">
              <p>No metadata found for <code>{slug}</code>.</p>
              <p>We can extend <code>src/data/books.manifest.json</code> later.</p>
            </div>
          )}
        </aside>

        {/* Placeholder de búsqueda in-app */}
        <aside className={`search-panel ${showSearch ? 'open' : ''}`}>
          <div className="info-panel__header">
            <h3>Search</h3>
            <button className="btn-ghost" onClick={onToggleSearch} aria-label="Close">×</button>
          </div>
          <div className="info-panel__body">
            <p>Coming soon: búsqueda dentro del texto con tu índice.</p>
          </div>
        </aside>
      </div>
    </div>
  )
}
