import { AlertTriangle, Bell, Camera, Package } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { api } from '../../lib/api'
import { StatTile } from '../../components/StatTile'
import { formatDateTime, alertBadgeClass, lotStatusLabel } from '../../lib/format'
import type { Alert, Lot } from '../../lib/types'

export function ExporterDashboard() {
  const lots = useQuery({
    queryKey: ['lots'],
    queryFn: async () => (await api.get<Lot[]>('/lots?limit=100')).data,
  })
  const alerts = useQuery({
    queryKey: ['alerts', 'active'],
    queryFn: async () => (await api.get<Alert[]>('/alerts/active?limit=50')).data,
  })

  const lotCount = lots.data?.length ?? 0
  const inTransport = lots.data?.filter(l => l.status === 'in_transport').length ?? 0
  const activeAlerts = alerts.data?.length ?? 0
  const critical = alerts.data?.filter(a => a.level === 'critical').length ?? 0

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Tableau de bord</h1>
        <p className="text-sm text-slate-500">
          Vue d'ensemble de vos lots d'ananas en circulation.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatTile label="Lots totaux" value={lotCount}
                  icon={<Package size={20} />} accent="brand" />
        <StatTile label="En transport" value={inTransport}
                  icon={<Camera size={20} />} accent="gold" />
        <StatTile label="Alertes actives" value={activeAlerts}
                  icon={<Bell size={20} />}
                  accent={activeAlerts > 0 ? 'gold' : 'brand'} />
        <StatTile label="Critiques" value={critical}
                  icon={<AlertTriangle size={20} />}
                  accent={critical > 0 ? 'red' : 'brand'} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentLots lots={lots.data?.slice(0, 5) ?? []}
                    loading={lots.isLoading} />
        <RecentAlerts alerts={alerts.data?.slice(0, 5) ?? []}
                      loading={alerts.isLoading} />
      </div>
    </div>
  )
}

function RecentLots({ lots, loading }: { lots: Lot[]; loading: boolean }) {
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-semibold text-slate-900">Derniers lots</h2>
        <Link to="/exporter/lots" className="text-sm text-brand-700 hover:underline">
          Voir tout →
        </Link>
      </div>
      {loading ? <Loading /> : lots.length === 0 ? <Empty label="Aucun lot" /> : (
        <ul className="divide-y divide-slate-100">
          {lots.map((lot) => (
            <li key={lot.id}>
              <Link to={`/exporter/lots/${lot.lot_code}`}
                    className="flex items-center justify-between py-3
                               hover:bg-slate-50 -mx-2 px-2 rounded-lg">
                <div>
                  <p className="font-medium text-slate-900">{lot.lot_code}</p>
                  <p className="text-xs text-slate-500">
                    {lot.producer_name} · {lot.quantity_kg} kg
                  </p>
                </div>
                <span className="badge-neutral">{lotStatusLabel(lot.status)}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

function RecentAlerts({ alerts, loading }: { alerts: Alert[]; loading: boolean }) {
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-semibold text-slate-900">Alertes actives</h2>
      </div>
      {loading ? <Loading /> : alerts.length === 0 ? (
        <Empty label="Aucune alerte active" />
      ) : (
        <ul className="divide-y divide-slate-100">
          {alerts.map((a) => (
            <li key={a.id} className="py-3">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-medium text-slate-900">{a.message}</p>
                  <p className="text-xs text-slate-500">
                    Lot {a.lot_id} · {formatDateTime(a.timestamp)}
                  </p>
                </div>
                <span className={alertBadgeClass(a.level)}>{a.level}</span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

const Loading = () => <p className="text-sm text-slate-400 py-6">Chargement…</p>
const Empty = ({ label }: { label: string }) =>
  <p className="text-sm text-slate-400 py-6">{label}</p>
