import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { ArrowLeft, Package, ShieldCheck, ThermometerSun } from 'lucide-react'
import { api } from '../../lib/api'
import { Logo } from '../../components/Logo'
import {
  formatDate, formatDateTime, lotStatusLabel, varietyLabel,
  verdictBadgeClass,
} from '../../lib/format'
import type { TracePayload } from '../../lib/types'

export function TracePage() {
  const { code } = useParams<{ code: string }>()
  const { data, isLoading, error } = useQuery({
    queryKey: ['public-trace', code],
    enabled: !!code,
    queryFn: async () =>
      (await api.get<TracePayload>(`/public/trace/${code}`)).data,
    retry: false,
  })

  return (
    <div className="min-h-screen bg-gradient-to-b from-brand-50 to-white">
      <header className="border-b border-brand-100 bg-white/70 backdrop-blur">
        <div className="mx-auto max-w-3xl px-4 py-4 flex items-center justify-between">
          <Logo />
          <Link to="/scan"
                className="text-sm text-brand-700 hover:underline
                           flex items-center gap-1">
            <ArrowLeft size={14} /> Scanner un autre lot
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-8 space-y-6">
        {isLoading && <p className="text-slate-500">Chargement…</p>}
        {error && (
          <div className="card p-6 text-center">
            <p className="text-slate-900 font-semibold">Lot introuvable</p>
            <p className="text-sm text-slate-500 mt-1">
              Vérifiez le code ou scannez à nouveau.
            </p>
          </div>
        )}
        {data && <TraceContent data={data} />}
      </main>

      <footer className="mx-auto max-w-3xl px-4 py-6 text-center text-xs
                         text-slate-400">
        Système de traçabilité AgriTraceBio · Bénin
      </footer>
    </div>
  )
}

function TraceContent({ data }: { data: TracePayload }) {
  const { lot, summary, inspections } = data
  const latestInspection = inspections[0]

  return (
    <>
      <div className="card p-6 space-y-3">
        <div className="flex items-center gap-3">
          <div className="rounded-full bg-brand-100 p-3">
            <Package className="text-brand-700" size={24} />
          </div>
          <div>
            <p className="text-xs uppercase tracking-wider text-slate-500">
              Lot
            </p>
            <p className="text-xl font-semibold">{lot.lot_code}</p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3 pt-2">
          <Info label="Producteur" value={lot.producer_name} />
          <Info label="Variété" value={varietyLabel(lot.variety)} />
          <Info label="Récolte" value={formatDate(lot.harvest_date)} />
          <Info label="Quantité" value={`${lot.quantity_kg} kg`} />
          <Info label="Origine" value={lot.origin_location} />
          <Info label="Destination" value={lot.destination ?? '—'} />
          <Info label="Statut" value={lotStatusLabel(lot.status)} />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3">
        <MiniStat label="Mesures IoT" value={summary.total_measurements} />
        <MiniStat label="Inspections IA" value={summary.total_inspections} />
        <MiniStat label="Alertes critiques" value={summary.critical_alerts}
                  warn={summary.critical_alerts > 0} />
      </div>

      {latestInspection && (
        <div className="card p-6">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-semibold text-slate-900">Dernier contrôle IA</h2>
            <span className={verdictBadgeClass(latestInspection.verdict)}>
              {latestInspection.verdict}
            </span>
          </div>
          <p className="text-sm text-slate-600">
            {latestInspection.detections.length} détection(s) le{' '}
            {formatDateTime(latestInspection.timestamp)}
          </p>
        </div>
      )}

      <div className="card p-6">
        <div className="flex items-center gap-2 mb-3">
          <ShieldCheck className="text-brand-600" size={18} />
          <h2 className="font-semibold text-slate-900">
            Blockchain de traçabilité
          </h2>
        </div>
        <p className="text-sm text-slate-600">
          Toutes les opérations sur ce lot sont enregistrées de manière
          infalsifiable dans notre blockchain. La transparence est garantie
          du champ au consommateur.
        </p>
      </div>

      <div className="card p-6">
        <div className="flex items-center gap-2 mb-3">
          <ThermometerSun className="text-gold-500" size={18} />
          <h2 className="font-semibold text-slate-900">
            Conditions de transport
          </h2>
        </div>
        <p className="text-sm text-slate-600">
          Ce lot est suivi en continu par des capteurs IoT (température,
          éthanol, qualité de l'air) et une intelligence artificielle qui
          analyse son état visuel tout au long de son acheminement.
        </p>
      </div>
    </>
  )
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs text-slate-500">{label}</p>
      <p className="text-sm text-slate-900">{value}</p>
    </div>
  )
}

function MiniStat({ label, value, warn }:
  { label: string; value: number; warn?: boolean }) {
  return (
    <div className={`card p-3 text-center ${
      warn ? 'bg-red-50 border-red-200' : ''
    }`}>
      <p className="text-2xl font-semibold">{value}</p>
      <p className="text-xs text-slate-500 mt-1">{label}</p>
    </div>
  )
}
