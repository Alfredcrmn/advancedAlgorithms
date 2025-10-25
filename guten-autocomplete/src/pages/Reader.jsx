// src/pages/Reader.jsx
import { useEffect, useMemo, useState, useCallback } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import Sidebar from '../components/Sidebar/Sidebar'
import Viewer from '../components/Viewer/Viewer'
import SearchResults from '../components/Sidebar/SearchResults'
import manifest from '../data/books.manifest.json'
import { paginateByChars } from '../utils/pagination'
import { useSearch } from '../state/useSearch'
import '../styles/reader.css'

// Une BASE_URL con una ruta relativa
function withBase(p) {
  const base = (import.meta.env.BASE_URL || '/').replace(/\/+$/, '')
  const path = String(p || '').replace(/^\/+/, '')
  return `${base}/${path}`
}

export default function Reader() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState('')
  const [pages, setPages]     = useState([])
  const [pageOffsets, setPageOffsets] = useState([])
  const [rawText, setRawText] = useState('')
  const [current, setCurrent] = useState(-1) // -1 = portada
  const [showInfo, setShowInfo] = useState(false)
  const [showSearch, setShowSearch] = useState(false)
  const [query, setQuery] = useState('')

  const bookMeta = useMemo(() => {
    if (!manifest || !Array.isArray(manifest)) return null
    return manifest.find(b => b.id === id) ?? null
  }, [id])

  const coverUrl = bookMeta ? withBase(bookMeta.coverPath) : ''
  const bookUrl  = bookMeta ? withBase(bookMeta.textPath)  : ''

  useEffect(() => {
    let active = true
    async function load() {
      try {
        setLoading(true); setError('')
        if (!bookMeta) throw new Error('Libro no encontrado en el manifiesto')
        const res = await fetch(bookUrl)
        if (!res.ok) throw new Error('No se pudo cargar el texto')
        const txt = await res.text()
        const { pages: pgs, pageOffsets: offs } = paginateByChars(txt)
        if (!active) return
        setRawText(txt)
        setPages(pgs)
        setPageOffsets(offs)
        setCurrent(-1) // portada
      } catch (e) {
        setError(String(e.message ?? e))
      } finally {
        setLoading(false)
      }
    }
    if (bookMeta) load()
    return () => { active = false }
  }, [bookMeta, bookUrl])

  const onHome = useCallback(() => navigate('/'), [navigate])
  const onToggleInfo = useCallback(() => setShowInfo(v => !v), [])
  const onToggleSearch = useCallback(() => setShowSearch(v => !v), [])

  // Navegación
  const atCover   = current < 0
  const atLast    = pages.length > 0 && current === pages.length - 1
  const canGoPrev = !atCover
  const canGoNext = atCover || !atLast

  const goPrev = useCallback(() => {
    setCurrent(p => (p < 0 ? p : p === 0 ? -1 : p - 1))
  }, [])
  const goNext = useCallback(() => {
    setCurrent(p => (p < 0 && pages.length > 0 ? 0 : p >= pages.length - 1 ? p : p + 1))
  }, [pages.length])

  // Teclas ← / →
  useEffect(() => {
    const onKey = (e) => {
      if (e.key === 'ArrowLeft')  { e.preventDefault(); if (canGoPrev) goPrev() }
      if (e.key === 'ArrowRight') { e.preventDefault(); if (canGoNext) goNext() }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [canGoPrev, canGoNext, goPrev, goNext])

  // Progreso %
  const progress = useMemo(() => {
    if (current < 0 || pages.length === 0) return 0
    return Math.floor(((current + 1) / pages.length) * 100)
  }, [current, pages.length])

  // Búsqueda exacta MVP
  const { results, elapsedMs, running } = useSearch(rawText, pageOffsets, query)

  // (opcional) si no existe el libro y ya no carga
  if (!bookMeta && !loading) {
    return (
      <main style={{ padding: 24 }}>
        <p>No se encontró el libro solicitado (<code>{id}</code>).</p>
        <button onClick={() => navigate('/')}>Volver</button>
      </main>
    )
  }

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

        {/* Panel Info */}
        <aside className={`info-panel ${showInfo ? 'open' : ''}`} aria-hidden={!showInfo}>
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
              <p>No metadata found for <code>{id}</code>.</p>
              <p>We can extend <code>src/data/books.manifest.json</code> later.</p>
            </div>
          )}
        </aside>

        {/* Panel Search */}
        <aside className={`search-panel ${showSearch ? 'open' : ''}`} aria-hidden={!showSearch}>
          <div className="info-panel__header">
            <h3>Search</h3>
            <button className="btn-ghost" onClick={onToggleSearch} aria-label="Close">×</button>
          </div>
          <div className="info-panel__body">
            <input
              type="search"
              placeholder="Buscar palabra o frase…"
              value={query}
              onChange={(e)=> setQuery(e.target.value)}
              className="input"
              autoFocus={showSearch}
            />
            <SearchResults
              query={query}
              running={running}
              elapsedMs={elapsedMs}
              results={results}
              onSelect={(r) => { setCurrent(r.pageIndex); setShowSearch(false); }}
            />
          </div>
        </aside>
      </div>
    </div>
  )
}

