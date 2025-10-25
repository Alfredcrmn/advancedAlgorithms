// src/components/LibraryCard.jsx
import { Link } from 'react-router-dom'

function withBase(p) {
  const base = (import.meta.env.BASE_URL || '/').replace(/\/+$/, '')
  const path = String(p || '').replace(/^\/+/, '')
  return `${base}/${path}`
}

export default function LibraryCard({ book }) {
  const coverUrl = withBase(book.coverPath)
  return (
    <Link className="bookCard" to={`/read/${book.id}`} title={`${book.title} — ${book.author}`}>
      <div className="bookCover" style={{ backgroundImage: `url(${coverUrl})` }} />
      <div className="bookMeta">
        <h3 className="bookTitle">{book.title}</h3>
        <p className="bookAuthor">{book.author}</p>
      </div>
    </Link>
  )
}
