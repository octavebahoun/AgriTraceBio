import { useEffect, useRef, useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { Logo } from '../../components/Logo'
import { Camera, CameraOff, ScanLine } from 'lucide-react'
import { Html5Qrcode } from 'html5-qrcode'

export function ScanPage() {
  const navigate = useNavigate()
  const [code, setCode] = useState('')
  const [scanning, setScanning] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const scannerRef = useRef<Html5Qrcode | null>(null)

  useEffect(() => {
    return () => { void stopScanner(scannerRef.current) }
  }, [])

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (code.trim()) navigate(`/trace/${code.trim()}`)
  }

  const start = async () => {
    setError(null)
    try {
      const el = document.getElementById('qr-reader')
      if (!el) return
      const scanner = new Html5Qrcode('qr-reader')
      scannerRef.current = scanner
      setScanning(true)
      await scanner.start(
        { facingMode: 'environment' },
        { fps: 10, qrbox: { width: 240, height: 240 } },
        onDecoded,
        () => { /* frame errors are noisy - ignore */ },
      )
    } catch {
      setError("Impossible d'accéder à la caméra.")
      setScanning(false)
    }
  }

  const onDecoded = (text: string) => {
    const code = extractLotCode(text)
    void stopScanner(scannerRef.current).then(() => {
      setScanning(false)
      if (code) navigate(`/trace/${code}`)
    })
  }

  const stop = async () => {
    await stopScanner(scannerRef.current)
    setScanning(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-brand-50 to-white
                    flex flex-col items-center px-4 py-8">
      <header className="w-full max-w-md flex justify-center mb-6">
        <Logo size={40} />
      </header>
      <div className="w-full max-w-md card p-6 space-y-6">
        <div className="text-center">
          <ScanLine className="mx-auto text-brand-600" size={40} />
          <h1 className="mt-3 text-xl font-semibold text-slate-900">
            Traçabilité de votre ananas
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Scannez le QR code pour connaître son origine.
          </p>
        </div>

        <div id="qr-reader" className="rounded-lg overflow-hidden bg-black" />

        {!scanning ? (
          <button onClick={start} className="btn-primary w-full">
            <Camera size={16} /> Activer la caméra
          </button>
        ) : (
          <button onClick={stop} className="btn-outline w-full">
            <CameraOff size={16} /> Arrêter
          </button>
        )}
        {error && <p className="text-sm text-red-600 text-center">{error}</p>}

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-slate-200" />
          </div>
          <div className="relative flex justify-center text-xs">
            <span className="bg-white px-2 text-slate-500">OU</span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-2">
          <label className="field-label">Saisir un code lot</label>
          <div className="flex gap-2">
            <input className="field-input flex-1" placeholder="AGR-001"
                   value={code} onChange={(e) => setCode(e.target.value)} />
            <button type="submit" className="btn-primary">Consulter</button>
          </div>
        </form>
      </div>
    </div>
  )
}

async function stopScanner(scanner: Html5Qrcode | null) {
  if (!scanner) return
  try { await scanner.stop(); scanner.clear() } catch { /* already stopped */ }
}

function extractLotCode(text: string): string | null {
  const trimmed = text.trim()
  const match = trimmed.match(/\/trace\/([^/?#]+)/)
  if (match) return match[1]
  if (/^[A-Za-z0-9_-]+$/.test(trimmed)) return trimmed
  return null
}
