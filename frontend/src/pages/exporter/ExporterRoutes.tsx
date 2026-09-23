import { LayoutDashboard, Package, ShieldCheck } from 'lucide-react'
import { Route, Routes } from 'react-router-dom'
import { AppLayout } from '../../components/AppLayout'
import type { NavItem } from '../../components/AppLayout'
import { ExporterDashboard } from './ExporterDashboard'
import { LotsListPage } from './LotsListPage'
import { LotDetailPage } from './LotDetailPage'
import { CreateLotPage } from './CreateLotPage'
import { BlockchainPage } from './BlockchainPage'

const nav: NavItem[] = [
  { to: '/exporter', label: 'Tableau de bord',
    icon: <LayoutDashboard size={18} /> },
  { to: '/exporter/lots', label: 'Lots',
    icon: <Package size={18} /> },
  { to: '/exporter/blockchain', label: 'Blockchain',
    icon: <ShieldCheck size={18} /> },
]

export function ExporterRoutes() {
  return (
    <AppLayout nav={nav}>
      <Routes>
        <Route index element={<ExporterDashboard />} />
        <Route path="lots" element={<LotsListPage />} />
        <Route path="lots/new" element={<CreateLotPage />} />
        <Route path="lots/:code" element={<LotDetailPage />} />
        <Route path="blockchain" element={<BlockchainPage />} />
      </Routes>
    </AppLayout>
  )
}
