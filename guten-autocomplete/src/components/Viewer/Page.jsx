// src/components/Viewer/Page.jsx

export default function Page({ content }) {
  // separa párrafos por doble salto para conservar bloques
  const blocks = content.split(/\n{2,}/).map(s => s.trim()).filter(Boolean)
  return (
    <article className="page">
      {blocks.map((p, i) => (
        <p key={i} className="page__p">{p}</p>
      ))}
    </article>
  )
}
