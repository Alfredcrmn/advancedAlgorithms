// src/layouts/AppLayout.jsx
import { Link, NavLink, Outlet } from 'react-router-dom'

export default function AppLayout() {
  return (
    <div className="appLayout">


      <Outlet />

    </div>
  )
}
