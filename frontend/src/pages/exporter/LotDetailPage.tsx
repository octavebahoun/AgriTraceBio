import { useQuery } from '@tanstack/react-query'
import { Link, useLocation, useParams } from 'react-router-dom'
import { ChevronLeft, Download, QrCode } from 'lucide-react'
import { api } from '../../lib/api'
import {
  alertBadgeClass, formatDate, formatDateTime, lotStatusLabel,
  varietyLabel, verdictBadgeClass,
} from '../../lib/format'
import type { TracePayload } from '../../lib/types'

export function LotDetailPage() {
  const { code } = useParams<{ code: string }>()
  const location = useLocation()
  const backTo = location.pathname.startsWith('/controller')
    ? '/controller/lots' : '/exporter/lots'
  const { data, isLoading } = useQuery({
    queryKey: ['trace', code],
    enabled: !!code,
    queryFn: async () =>
      (await api.get<TracePayload>(`/public/trace/${code}`)).data,
  })

  if (isLoading) return <p className="text-slate-500">Chargement…</p>
  if (!data) return <p className="text-slate-500">Lot introuvable.</p>

  const { lot, measurements, alerts, inspections, summary } = data

  const downloadCertificate = async () => {
    const res = await api.get(`/certificates/lot/${lot.lot_code}.pdf`, {
      responseType: 'blob',
    })
    const url = URL.createObjectURL(res.data as Blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `certificat_${lot.lot_code}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <Link to={backTo}
            className="inline-flex items-center gap-1 text-sm text-slate-600
                       hover:text-slate-900">
        <ChevronLeft size={16} /> Retour aux lots
      </Link>

      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">
            Lot {lot.lot_code}
          </h1>
          <p className="text-sm text-slate-500">
            {lot.producer_name} · {varietyLabel(lot.variety)} · {lot.quantity_kg} kg
          </p>
        </div>
        <div className="flex gap-2">
          <a href={`/api/lots/code/${lot.lot_code}/qr.svg`} target="_blank"
             rel="noreferrer" className="btn-outline">
            <QrCode size={16} /> QR code
          </a>
          <button onClick={downloadCertificate} className="btn-primary">
            <Download size={16} /> Certificat PDF
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <KPI label="Statut" value={lotStatusLabel(lot.status)} />
        <KPI label="Récolte" value={formatDate(lot.harvest_date)} />
        <KPI label="Origine" value={lot.origin_location} />
        <KPI label="Destination" value={lot.destination ?? '—'} />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <KPI label="Mesures" value={summary.total_measurements} />
        <KPI label="Alertes" value={summary.total_alerts} />
        <KPI label="Critiques" value={summary.critical_alerts}
             warn={summary.critical_alerts > 0} />
        <KPI label="Inspections rejetées" value={summary.rejected_inspections}
             warn={summary.rejected_inspections > 0} />
      </div>

      <Section title="Dernières mesures IoT">
        {measurements.length === 0 ? <Empty /> : (
          <table className="w-full text-sm">
            <thead className="text-slate-500">
              <tr><Th>Date</Th><Th>Temp.</Th><Th>Éthanol</Th>
                  <Th>Air</Th><Th>Device</Th></tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {measurements.slice(0, 10).map((m) => (
                <tr key={m.id}>
                  <Td>{formatDateTime(m.timestamp)}</Td>
                  <Td>{m.temperature.toFixed(1)} °C</Td>
                  <Td>{m.ethanol_ppm.toFixed(0)} ppm</Td>
                  <Td>{m.air_quality_ppm.toFixed(0)} ppm</Td>
                  <Td>{m.device_id}</Td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Section>

      <Section title="Alertes">
        {alerts.length === 0 ? <Empty /> : (
          <ul className="divide-y divide-slate-100">
            {alerts.slice(0, 10).map((a) => (
              <li key={a.id} className="py-3 flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm text-slate-900">{a.message}</p>
                  <p className="text-xs text-slate-500">
                    {formatDateTime(a.timestamp)} · seuil {a.threshold}
                  </p>
                </div>
                <span className={alertBadgeClass(a.level)}>{a.level}</span>
              </li>
            ))}
          </ul>
        )}
      </Section>

      <Section title="Inspections vision par ordinateur">
        {inspections.length === 0 ? <Empty /> : (
          <ul className="divide-y divide-slate-100">
            {inspections.slice(0, 10).map((i) => (
              <li key={i.id} className="py-3 flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm text-slate-900">
                    {i.detections.length} détection(s) · modèle {i.model_version}
                  </p>
                  <p className="text-xs text-slate-500">
                    {formatDateTime(i.timestamp)} · device {i.device_id}
                  </p>
                </div>
                <span className={verdictBadgeClass(i.verdict)}>{i.verdict}</span>
              </li>
            ))}
          </ul>
        )}
      </Section>
    </div>
  )
}

function KPI({ label, value, warn }:
  { label: string; value: string | number; warn?: boolean }) {
  return (
    <div className={`card p-4 ${warn ? 'border-red-200 bg-red-50' : ''}`}>
      <p className="text-xs text-slate-500">{label}</p>
      <p className={`text-lg font-semibold ${
        warn ? 'text-red-700' : 'text-slate-900'
      }`}>{value}</p>
    </div>
  )
}

const Section = ({ title, children }:
  { title: string; children: React.ReactNode }) => (
  <div className="card p-5">
    <h2 className="font-semibold text-slate-900 mb-3">{title}</h2>
    {children}
  </div>
)
const Th = ({ children }: { children: React.ReactNode }) =>
  <th className="text-left font-medium py-2">{children}</th>
const Td = ({ children }: { children: React.ReactNode }) =>
  <td className="py-2">{children}</td>
const Empty = () => <p className="text-sm text-slate-400 py-2">Aucune donnée.</p>
