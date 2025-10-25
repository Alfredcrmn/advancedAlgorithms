// src/components/LibraryCard.jsx
export default function LibraryCard({ book }) {
  return (
    <a className="bookCard" href={`/read/${book.id}`} title={`${book.title} — ${book.author}`}>
      <div className="bookCover" style={{ backgroundImage: `url(${book.coverPath})` }} />
      <div className="bookMeta">
        <h3 className="bookTitle">{book.title}</h3>
        <p className="bookAuthor">{book.author}</p>
      </div>
    </a>
  )
}
