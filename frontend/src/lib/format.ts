import type { AlertLevel, InspectionVerdict } from './types'

export function formatDate(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleDateString('fr-FR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  })
}

export function formatDateTime(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleString('fr-FR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

export function alertBadgeClass(level: AlertLevel): string {
  if (level === 'critical') return 'badge-crit'
  if (level === 'warning') return 'badge-warn'
  return 'badge-neutral'
}

export function verdictBadgeClass(v: InspectionVerdict): string {
  if (v === 'rejected') return 'badge-crit'
  if (v === 'warning') return 'badge-warn'
  return 'badge-ok'
}

export function lotStatusLabel(s: string): string {
  const map: Record<string, string> = {
    created: 'Créé',
    in_transport: 'En transport',
    delivered: 'Livré',
    rejected: 'Rejeté',
  }
  return map[s] ?? s
}

export function varietyLabel(v: string): string {
  return v === 'cayenne_lisse' ? 'Cayenne lisse' : 'Pain de sucre'
}
