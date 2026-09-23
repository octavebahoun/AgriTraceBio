import { createContext, useContext, useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { api, authStorage } from '../lib/api'
import type { User } from '../lib/types'

interface AuthContextValue {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<User>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = authStorage.get()
    if (!token) { setLoading(false); return }
    api.get<User>('/auth/me')
      .then((r) => setUser(r.data))
      .catch(() => authStorage.clear())
      .finally(() => setLoading(false))
  }, [])

  const login = async (email: string, password: string) => {
    const r = await api.post<{ token: string; user: User }>(
      '/auth/login', { email, password }
    )
    authStorage.set(r.data.token)
    setUser(r.data.user)
    return r.data.user
  }

  const logout = () => {
    authStorage.clear()
    setUser(null)
    window.location.href = '/login'
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
