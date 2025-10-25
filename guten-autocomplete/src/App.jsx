// src/App.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Home from './pages/Home'
import Reader from './pages/Reader'
import NotFound from './pages/NotFound'
import AppLayout from './layouts/AppLayout'

// estilos globales
import './styles/base.css'
import './styles/layout.css'
import './styles/components.css'

function ScrollToTop() {
  const { pathname } = window.location

  return null
}

export default function App() {
  return (
    <Router>
      <ScrollToTop />
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/read/:slug" element={<Reader />} />
        </Route>

        {/* alias opcional */}
        <Route path="/home" element={<Navigate to="/" replace />} />

        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}
