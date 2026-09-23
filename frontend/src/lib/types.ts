export type UserRole = 'admin' | 'exporter' | 'controller'

export interface User {
  id: string
  email: string
  name: string
  role: UserRole
  created_at: string
}

export interface Lot {
  id: string
  lot_code: string
  producer_name: string
  variety: 'cayenne_lisse' | 'pain_de_sucre'
  harvest_date: string
  quantity_kg: number
  origin_location: string
  destination: string | null
  exporter_id: string
  status: 'created' | 'in_transport' | 'delivered' | 'rejected'
  created_at: string
  updated_at: string
}

export interface Measurement {
  id: string
  lot_id: string
  temperature: number
  ethanol_ppm: number
  air_quality_ppm: number
  device_id: string
  timestamp: string
}

export type AlertLevel = 'info' | 'warning' | 'critical'
export type AlertType = 'temperature' | 'ethanol' | 'air_quality'

export interface Alert {
  id: string
  lot_id: string
  alert_type: AlertType
  level: AlertLevel
  message: string
  value: number
  threshold: number
  timestamp: string
  resolved: boolean
}

export type InspectionVerdict = 'ok' | 'warning' | 'rejected'

export interface Detection {
  class_label: string
  confidence: number
  bbox: number[]
}

export interface Inspection {
  id: string
  lot_code: string
  device_id: string
  detections: Detection[]
  verdict: InspectionVerdict
  model_version: string
  image_path: string | null
  timestamp: string
}

export interface TracePayload {
  lot: Lot
  measurements: Measurement[]
  alerts: Alert[]
  inspections: Inspection[]
  summary: {
    total_measurements: number
    total_alerts: number
    critical_alerts: number
    total_inspections: number
    rejected_inspections: number
  }
}
