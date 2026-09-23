import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Check } from 'lucide-react'
import { api } from '../../lib/api'
import { alertBadgeClass, formatDateTime } from '../../lib/format'
import type { Alert } from '../../lib/types'

export function AlertsPage() {
  const qc = useQueryClient()
  const { data, isLoading } = useQuery({
    queryKey: ['alerts', 'active'],
    queryFn: async () =>
      (await api.get<Alert[]>('/alerts/active?limit=100')).data,
  })

  const resolve = useMutation({
    mutationFn: (id: string) => api.post(`/alerts/${id}/resolve`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['alerts'] }),
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">
          Alertes actives
        </h1>
        <p className="text-sm text-slate-500">
          Consultez et résolvez les anomalies détectées sur les lots en transport.
        </p>
      </div>

      <div className="card overflow-hidden">
        {isLoading ? (
          <p className="p-6 text-slate-400 text-sm">Chargement…</p>
        ) : (data?.length ?? 0) === 0 ? (
          <p className="p-6 text-slate-400 text-sm">
            Aucune alerte active. Tout est nominal.
          </p>
        ) : (
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-slate-600">
              <tr>
                <Th>Lot</Th><Th>Type</Th><Th>Niveau</Th>
                <Th>Message</Th><Th>Date</Th><Th>{' '}</Th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {data!.map((a) => (
                <tr key={a.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium">{a.lot_id}</td>
                  <td className="px-4 py-3">{a.alert_type}</td>
                  <td className="px-4 py-3">
                    <span className={alertBadgeClass(a.level)}>{a.level}</span>
                  </td>
                  <td className="px-4 py-3 max-w-md truncate" title={a.message}>
                    {a.message}
                  </td>
                  <td className="px-4 py-3 text-slate-500">
                    {formatDateTime(a.timestamp)}
                  </td>
                  <td className="px-4 py-3">
                    <button onClick={() => resolve.mutate(a.id)}
                            disabled={resolve.isPending}
                            className="btn-outline text-xs !py-1 !px-2">
                      <Check size={14} /> Résoudre
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

const Th = ({ children }: { children: React.ReactNode }) =>
  <th className="px-4 py-3 text-left font-medium">{children}</th>
