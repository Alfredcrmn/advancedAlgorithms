// src/components/Viewer/Viewer.jsx

import Page from './Page'

export default function Viewer({ loading, error, coverUrl, pages, currentPage }) {
  const total = pages.length
  const atCover = currentPage < 0

  const footerLabel = atCover
    ? 'Cover'
    : (total ? `Page ${currentPage + 1} / ${total}` : '')

  return (
    <div className="viewer">
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
          <div className="viewer__footer">{footerLabel}</div>
        </>
      )}
    </div>
  )
}
