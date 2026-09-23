import type { ReactNode } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { LogOut } from 'lucide-react'
import { Logo } from './Logo'
import { useAuth } from '../contexts/AuthContext'

export interface NavItem {
  to: string
  label: string
  icon: ReactNode
}

interface AppLayoutProps {
  nav: NavItem[]
  children: ReactNode
}

export function AppLayout({ nav, children }: AppLayoutProps) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="min-h-screen flex bg-slate-50">
      <aside className="w-64 shrink-0 border-r border-slate-200 bg-white
                        flex flex-col">
        <div className="p-5 border-b border-slate-200">
          <button onClick={() => navigate('/')} className="w-full text-left">
            <Logo />
          </button>
        </div>
        <nav className="flex-1 p-3 space-y-1">
          {nav.map((item) => (
            <NavLink key={item.to} to={item.to} end
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2 text-sm
                 transition-colors ${
                  isActive
                    ? 'bg-brand-50 text-brand-800 font-medium'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}>
              {item.icon}
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="p-3 border-t border-slate-200">
          <div className="px-3 py-2 mb-2">
            <p className="text-sm font-medium text-slate-900 truncate">
              {user?.name}
            </p>
            <p className="text-xs text-slate-500 truncate capitalize">
              {user?.role}
            </p>
          </div>
          <button onClick={logout}
            className="w-full flex items-center gap-3 rounded-lg px-3 py-2
                       text-sm text-slate-600 hover:bg-slate-100">
            <LogOut size={16} />
            <span>Déconnexion</span>
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-auto">
        <div className="mx-auto max-w-6xl p-6 md:p-10">{children}</div>
      </main>
    </div>
  )
}
