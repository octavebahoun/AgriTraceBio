import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChevronLeft } from 'lucide-react'
import { AxiosError } from 'axios'
import { api } from '../../lib/api'

export function CreateLotPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    lot_code: '', producer_name: '', variety: 'cayenne_lisse',
    harvest_date: '', quantity_kg: '', origin_location: '',
    exporter_id: '', destination: '',
  })
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  const set = (k: string, v: string) => setForm({ ...form, [k]: v })

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      await api.post('/lots', {
        ...form,
        quantity_kg: Number(form.quantity_kg),
        harvest_date: new Date(form.harvest_date).toISOString(),
        destination: form.destination || undefined,
      })
      navigate('/exporter/lots')
    } catch (err) {
      const ax = err as AxiosError<{ error?: string }>
      setError(ax.response?.data?.error === 'lot_code_already_exists'
        ? 'Ce code lot existe déjà.'
        : 'Erreur lors de la création.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="max-w-2xl space-y-6">
      <button onClick={() => navigate(-1)}
              className="flex items-center gap-1 text-sm text-slate-600
                         hover:text-slate-900">
        <ChevronLeft size={16} /> Retour
      </button>
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Nouveau lot</h1>
        <p className="text-sm text-slate-500">
          Enregistrez un nouveau lot d'ananas.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="card p-6 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Field label="Code lot" required value={form.lot_code}
                 onChange={(v) => set('lot_code', v)} placeholder="AGR-001" />
          <Field label="Producteur" required value={form.producer_name}
                 onChange={(v) => set('producer_name', v)} />
          <div>
            <label className="field-label">Variété</label>
            <select className="field-input" value={form.variety}
                    onChange={(e) => set('variety', e.target.value)}>
              <option value="cayenne_lisse">Cayenne lisse</option>
              <option value="pain_de_sucre">Pain de sucre</option>
            </select>
          </div>
          <Field label="Date de récolte" required type="date"
                 value={form.harvest_date}
                 onChange={(v) => set('harvest_date', v)} />
          <Field label="Quantité (kg)" required type="number"
                 value={form.quantity_kg}
                 onChange={(v) => set('quantity_kg', v)} />
          <Field label="Origine (commune)" required value={form.origin_location}
                 onChange={(v) => set('origin_location', v)} placeholder="Allada" />
          <Field label="ID exportateur" required value={form.exporter_id}
                 onChange={(v) => set('exporter_id', v)} placeholder="EXP-01" />
          <Field label="Destination" value={form.destination}
                 onChange={(v) => set('destination', v)} placeholder="Rungis" />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <button type="button" onClick={() => navigate(-1)}
                  className="btn-outline">Annuler</button>
          <button type="submit" disabled={submitting} className="btn-primary">
            {submitting ? 'Création…' : 'Créer le lot'}
          </button>
        </div>
      </form>
    </div>
  )
}

interface FieldProps {
  label: string
  value: string
  onChange: (v: string) => void
  type?: string
  required?: boolean
  placeholder?: string
}

function Field({ label, value, onChange, type, required, placeholder }: FieldProps) {
  return (
    <div>
      <label className="field-label">{label}{required && ' *'}</label>
      <input className="field-input" type={type ?? 'text'} required={required}
             value={value} placeholder={placeholder}
             onChange={(e) => onChange(e.target.value)} />
    </div>
  )
}
