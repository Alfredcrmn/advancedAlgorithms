// src/components/Sidebar/Sidebar.jsx

import { useMemo } from 'react'

function Icon({ name }) {
  // SVGs minimalistas para no depender de librerías
  const map = useMemo(() => ({
    menu: (
      <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
        <path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round"/>
      </svg>
    ),
    home: (
      <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
        <path d="M3 10.5 12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1v-10.5z" stroke="currentColor" strokeWidth="2" fill="none" strokeLinejoin="round"/>
      </svg>
    ),
    info: (
      <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
        <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2" fill="none"/>
        <path d="M12 8h.01M11 12h2v6h-2z" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round"/>
      </svg>
    ),
    search: (
      <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
        <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" fill="none"/>
        <path d="M20 20l-3.5-3.5" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round"/>
      </svg>
    ),
  }), [])

  return map[name] ?? null
}

export default function Sidebar({ onHome, onInfoToggle, onSearchToggle }) {
  return (
    <nav className="sidebar" aria-label="Reader navigation">
      <ul>
        <li className="sidebar__item sidebar__item--ghost" title="Menu">
          <div className="sidebar__icon"><Icon name="menu" /></div>
          <span className="sidebar__label">Menu</span>
        </li>

        <li className="sidebar__item">
          <button className="sidebar__btn" onClick={onHome} title="Home" aria-label="Home">
            <div className="sidebar__icon"><Icon name="home" /></div>
            <span className="sidebar__label">Home</span>
          </button>
        </li>

        <li className="sidebar__item">
          <button className="sidebar__btn" onClick={onInfoToggle} title="Book info" aria-label="Book info">
            <div className="sidebar__icon"><Icon name="info" /></div>
            <span className="sidebar__label">Info</span>
          </button>
        </li>

        <li className="sidebar__item">
          <button className="sidebar__btn" onClick={onSearchToggle} title="Search in book" aria-label="Search">
            <div className="sidebar__icon"><Icon name="search" /></div>
            <span className="sidebar__label">Search</span>
          </button>
        </li>
      </ul>
    </nav>
  )
}
