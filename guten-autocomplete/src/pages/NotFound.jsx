// src/pages/NotFound.jsx
import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <main style={{ minHeight: '70vh', display: 'grid', placeItems: 'center' }}>
      <div style={{ textAlign: 'center', maxWidth: 520 }}>
        <h1 style={{ marginBottom: 8 }}>404</h1>
        <p style={{ opacity: 0.8, marginBottom: 16 }}>
          La página que buscas no existe o ha cambiado.
        </p>
        <Link to="/" style={{
          padding: '10px 14px',
          background: '#8ab4ff',
          color: '#0b1022',
          borderRadius: 8,
          textDecoration: 'none',
          fontWeight: 600
        }}>
          Volver al inicio
        </Link>
      </div>
    </main>
  )
}
