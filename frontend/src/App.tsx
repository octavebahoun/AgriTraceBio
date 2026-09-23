import { Navigate, Route, Routes } from 'react-router-dom'
import { LoginPage } from './pages/LoginPage'
import { ProtectedRoute } from './components/ProtectedRoute'
import { useAuth } from './contexts/AuthContext'
import { ExporterRoutes } from './pages/exporter/ExporterRoutes'
import { ControllerRoutes } from './pages/controller/ControllerRoutes'
import { TracePage } from './pages/public/TracePage'
import { ScanPage } from './pages/public/ScanPage'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/scan" element={<ScanPage />} />
      <Route path="/trace/:code" element={<TracePage />} />
      <Route
        path="/exporter/*"
        element={
          <ProtectedRoute allowedRoles={['exporter', 'admin']}>
            <ExporterRoutes />
          </ProtectedRoute>
        }
      />
      <Route
        path="/controller/*"
        element={
          <ProtectedRoute allowedRoles={['controller', 'admin']}>
            <ControllerRoutes />
          </ProtectedRoute>
        }
      />
      <Route path="/" element={<HomeRedirect />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

function HomeRedirect() {
  const { user, loading } = useAuth()
  if (loading) return null
  if (!user) return <Navigate to="/scan" replace />
  if (user.role === 'controller') return <Navigate to="/controller" replace />
  return <Navigate to="/exporter" replace />
}
