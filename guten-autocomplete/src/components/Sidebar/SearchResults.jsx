//src/components/Sidebar/SearchResults.jsx

export default function SearchResults({ query, running, elapsedMs, results, onSelect }) {
  return (
    <div className="searchResults">
      <div className="searchResults__meta">
        {running ? 'Buscando…' : (
          query
            ? `${results.length} resultados · ${elapsedMs} ms`
            : 'Escribe para buscar'
        )}
      </div>

      <ul className="searchResults__list">
        {results.map((r, i) => (
          <li key={r.pos + ':' + i} className="searchResults__item">
            <button
              className="searchResults__btn"
              onClick={() => onSelect?.(r)}
              title={`Ir a la página ${r.pageIndex + 1}`}
            >
              <span className="searchResults__page">Pg {r.pageIndex + 1}</span>
              <span className="searchResults__snippet">
                {r.before} <mark>{r.match}</mark> {r.after}
              </span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
