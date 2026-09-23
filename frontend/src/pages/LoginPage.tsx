import { useState } from 'react'
import type { FormEvent } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { Logo } from '../components/Logo'
import { useAuth } from '../contexts/AuthContext'

export function LoginPage() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  if (user) return <Navigate to={homeFor(user.role)} replace />

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      const u = await login(email, password)
      navigate(homeFor(u.role), { replace: true })
    } catch {
      setError('Identifiants invalides.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-brand-50 p-6">
      <div className="w-full max-w-md card p-8">
        <div className="flex justify-center mb-6"><Logo size={40} /></div>
        <h1 className="text-xl font-semibold text-center text-slate-900">
          Se connecter
        </h1>
        <p className="text-sm text-slate-500 text-center mb-6">
          Plateforme de traçabilité ananas — Bénin
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="field-label">Email</label>
            <input type="email" required autoFocus className="field-input"
                   value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <label className="field-label">Mot de passe</label>
            <input type="password" required className="field-input"
                   value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button type="submit" disabled={submitting}
                  className="btn-primary w-full">
            {submitting ? 'Connexion…' : 'Se connecter'}
          </button>
        </form>
      </div>
    </div>
  )
}

function homeFor(role: string): string {
  if (role === 'controller') return '/controller'
  if (role === 'admin' || role === 'exporter') return '/exporter'
  return '/'
}
