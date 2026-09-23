import { Bell, Package, ShieldCheck } from 'lucide-react'
import { Route, Routes } from 'react-router-dom'
import { AppLayout } from '../../components/AppLayout'
import type { NavItem } from '../../components/AppLayout'
import { AlertsPage } from './AlertsPage'
import { ControllerLotsPage } from './ControllerLotsPage'
import { ControllerLotDetail } from './ControllerLotDetail'
import { BlockchainPage } from '../exporter/BlockchainPage'

const nav: NavItem[] = [
  { to: '/controller', label: 'Alertes actives',
    icon: <Bell size={18} /> },
  { to: '/controller/lots', label: 'Lots',
    icon: <Package size={18} /> },
  { to: '/controller/blockchain', label: 'Blockchain',
    icon: <ShieldCheck size={18} /> },
]

export function ControllerRoutes() {
  return (
    <AppLayout nav={nav}>
      <Routes>
        <Route index element={<AlertsPage />} />
        <Route path="lots" element={<ControllerLotsPage />} />
        <Route path="lots/:code" element={<ControllerLotDetail />} />
        <Route path="blockchain" element={<BlockchainPage />} />
      </Routes>
    </AppLayout>
  )
}
