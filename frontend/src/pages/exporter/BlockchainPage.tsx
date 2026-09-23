import { useQuery } from '@tanstack/react-query'
import { CheckCircle2, XCircle } from 'lucide-react'
import { api } from '../../lib/api'
import { formatDateTime } from '../../lib/format'

interface Block {
  index: number
  event_type: string
  lot_code: string | null
  hash: string
  previous_hash: string
  timestamp: string
}

interface VerifyResult {
  valid: boolean
  total_blocks: number
  broken_at_index: number | null
  reason: string | null
}

export function BlockchainPage() {
  const blocks = useQuery({
    queryKey: ['blockchain'],
    queryFn: async () =>
      (await api.get<Block[]>('/blockchain?limit=100')).data,
  })
  const verify = useQuery({
    queryKey: ['blockchain', 'verify'],
    queryFn: async () => {
      try {
        return (await api.get<VerifyResult>('/blockchain/verify')).data
      } catch (e) {
        const err = e as { response?: { data?: VerifyResult } }
        return err.response?.data ?? null
      }
    },
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Blockchain</h1>
        <p className="text-sm text-slate-500">
          Chaîne d'événements infalsifiable de toutes les opérations.
        </p>
      </div>

      {verify.data && (
        <div className={`card p-5 flex items-start gap-4 ${
          verify.data.valid ? 'border-brand-200 bg-brand-50' :
                              'border-red-200 bg-red-50'
        }`}>
          {verify.data.valid
            ? <CheckCircle2 size={28} className="text-brand-600" />
            : <XCircle size={28} className="text-red-600" />}
          <div>
            <p className="font-semibold text-slate-900">
              {verify.data.valid
                ? 'Chaîne intègre'
                : 'Compromise ! Falsification détectée'}
            </p>
            <p className="text-sm text-slate-700">
              {verify.data.total_blocks} blocs vérifiés
              {verify.data.reason && ` · ${verify.data.reason}`}
            </p>
          </div>
        </div>
      )}

      <div className="card overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr>
              <Th>#</Th><Th>Événement</Th><Th>Lot</Th>
              <Th>Date</Th><Th>Hash</Th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {blocks.data?.map((b) => (
              <tr key={b.index} className="hover:bg-slate-50">
                <td className="px-4 py-3 font-mono">{b.index}</td>
                <td className="px-4 py-3">{b.event_type}</td>
                <td className="px-4 py-3">{b.lot_code ?? '—'}</td>
                <td className="px-4 py-3">{formatDateTime(b.timestamp)}</td>
                <td className="px-4 py-3 font-mono text-xs text-slate-500">
                  {b.hash.slice(0, 16)}…
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
