import type { ReactNode } from 'react'

interface StatTileProps {
  label: string
  value: string | number
  icon?: ReactNode
  hint?: string
  accent?: 'brand' | 'gold' | 'red' | 'slate'
}

const accentMap: Record<string, string> = {
  brand: 'text-brand-700 bg-brand-50',
  gold: 'text-gold-500 bg-amber-50',
  red: 'text-red-700 bg-red-50',
  slate: 'text-slate-700 bg-slate-100',
}

export function StatTile({ label, value, icon, hint, accent = 'brand' }: StatTileProps) {
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">{label}</p>
          <p className="mt-1 text-3xl font-semibold text-slate-900">{value}</p>
          {hint && <p className="mt-1 text-xs text-slate-500">{hint}</p>}
        </div>
        {icon && (
          <div className={`rounded-lg p-3 ${accentMap[accent]}`}>{icon}</div>
        )}
      </div>
    </div>
  )
}
