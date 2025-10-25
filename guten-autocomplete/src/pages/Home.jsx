import manifest from '../data/books.manifest.json'
import LibraryCard from '../components/LibraryCard'

export default function Home() {
  return (
    <main className="landing">
      <div className="landing-grid">
        <section className="introCard">
          <h1>Web eBook Reader</h1>
          <p>
            Explore a curated library of classic literature and enjoy reading
            without distractions.
          </p>
          <p>
            Search for any word or phrase across the entire collection and jump
            directly to its occurrences within the books.
          </p>
          <a className="introCta" href="#library">Ver biblioteca</a>
        </section>

        <div id="library" className="cards">
          {manifest.map(book => (
            <LibraryCard key={book.id} book={book} />
          ))}
        </div>
      </div>
    </main>
  )
}
