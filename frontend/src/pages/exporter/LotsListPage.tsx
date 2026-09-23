import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Plus } from 'lucide-react'
import { api } from '../../lib/api'
import { formatDate, lotStatusLabel, varietyLabel } from '../../lib/format'
import type { Lot } from '../../lib/types'

export function LotsListPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['lots'],
    queryFn: async () => (await api.get<Lot[]>('/lots?limit=200')).data,
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Lots</h1>
          <p className="text-sm text-slate-500">
            Suivi de vos lots d'ananas de la récolte à la livraison.
          </p>
        </div>
        <Link to="/exporter/lots/new" className="btn-primary">
          <Plus size={16} /> Nouveau lot
        </Link>
      </div>

      <div className="card overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr>
              <Th>Code</Th><Th>Producteur</Th><Th>Variété</Th>
              <Th>Récolte</Th><Th>Quantité</Th><Th>Statut</Th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {isLoading && (
              <tr><td colSpan={6} className="p-6 text-center text-slate-400">
                Chargement…
              </td></tr>
            )}
            {!isLoading && (data?.length ?? 0) === 0 && (
              <tr><td colSpan={6} className="p-6 text-center text-slate-400">
                Aucun lot. Créez le premier avec le bouton ci-dessus.
              </td></tr>
            )}
            {data?.map((lot) => (
              <tr key={lot.id} className="hover:bg-slate-50">
                <td className="px-4 py-3 font-medium">
                  <Link to={`/exporter/lots/${lot.lot_code}`}
                        className="text-brand-700 hover:underline">
                    {lot.lot_code}
                  </Link>
                </td>
                <td className="px-4 py-3">{lot.producer_name}</td>
                <td className="px-4 py-3">{varietyLabel(lot.variety)}</td>
                <td className="px-4 py-3">{formatDate(lot.harvest_date)}</td>
                <td className="px-4 py-3">{lot.quantity_kg} kg</td>
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
