// src/components/Viewer/Viewer.jsx

import { useEffect, useMemo, useRef, useState } from 'react'
import Page from './Page'

export default function Viewer({ loading, error, coverUrl, pages, currentPage, setCurrentPage }) {
  const total = pages.length
  const containerRef = useRef(null)
  const [hovering, setHovering] = useState(false)

  const atCover = currentPage < 0
  const atFirst = currentPage === 0
  const atLast  = currentPage === total - 1

  function goPrev() {
    if (atCover) return
    if (atFirst) { setCurrentPage(-1); return }
    setCurrentPage(p => Math.max(0, p - 1))
  }
  function goNext() {
    if (atCover) { setCurrentPage(0); return }
    if (!atLast) setCurrentPage(p => Math.min(total - 1, p + 1))
  }

  useEffect(() => {
    function onKey(e) {
      if (e.key === 'ArrowLeft')  { e.preventDefault(); goPrev() }
      if (e.key === 'ArrowRight') { e.preventDefault(); goNext() }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  })

  const footerLabel = useMemo(() => {
    if (atCover) return 'Cover'
    if (total === 0) return ''
    return `Page ${currentPage + 1} / ${total}`
  }, [atCover, currentPage, total])

  return (
    <div
      className="viewer"
      ref={containerRef}
      onMouseEnter={() => setHovering(true)}
      onMouseLeave={() => setHovering(false)}
    >
      {loading && <div className="viewer__status">Loading…</div>}
      {error && !loading && <div className="viewer__status viewer__status--error">{error}</div>}

      {!loading && !error && (
        <>
          <div className="viewer__page">
            {atCover ? (
              <img src={coverUrl} alt="Book cover" className="viewer__cover" />
            ) : (
              <Page content={pages[currentPage]} />
            )}
          </div>

          {/* Botones de navegación (solo visibles al hover) */}
          <button
            className={`nav-btn nav-btn--left ${hovering ? 'show' : ''}`}
            onClick={goPrev}
            disabled={atCover}
            aria-label="Previous page"
          >
            ‹
          </button>
          <button
            className={`nav-btn nav-btn--right ${hovering ? 'show' : ''}`}
            onClick={goNext}
            disabled={atLast && !atCover}
            aria-label="Next page"
          >
            ›
          </button>

          <div className="viewer__footer">{footerLabel}</div>
        </>
      )}
    </div>
  )
}
/* src/components/Viewer/Viewer.jsx */