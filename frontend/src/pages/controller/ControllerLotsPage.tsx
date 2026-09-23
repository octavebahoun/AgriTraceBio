import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { api } from '../../lib/api'
import { formatDate, lotStatusLabel, varietyLabel } from '../../lib/format'
import type { Lot } from '../../lib/types'

export function ControllerLotsPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['lots'],
    queryFn: async () => (await api.get<Lot[]>('/lots?limit=200')).data,
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Lots</h1>
        <p className="text-sm text-slate-500">
          Consultez la traçabilité de chaque lot.
        </p>
      </div>

      <div className="card overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr>
              <Th>Code</Th><Th>Producteur</Th><Th>Variété</Th>
              <Th>Récolte</Th><Th>Statut</Th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {isLoading && (
              <tr><td colSpan={5} className="p-6 text-center text-slate-400">
                Chargement…
              </td></tr>
            )}
            {data?.map((lot) => (
              <tr key={lot.id} className="hover:bg-slate-50">
                <td className="px-4 py-3">
                  <Link to={`/controller/lots/${lot.lot_code}`}
                        className="text-brand-700 hover:underline font-medium">
                    {lot.lot_code}
                  </Link>
                </td>
                <td className="px-4 py-3">{lot.producer_name}</td>
                <td className="px-4 py-3">{varietyLabel(lot.variety)}</td>
                <td className="px-4 py-3">{formatDate(lot.harvest_date)}</td>
                <td className="px-4 py-3">
                  <span className="badge-neutral">
                    {lotStatusLabel(lot.status)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

const Th = ({ children }: { children: React.ReactNode }) =>
  <th className="px-4 py-3 text-left font-medium">{children}</th>
