import { LotDetailPage } from '../exporter/LotDetailPage'

// Le contrôleur voit exactement les mêmes infos que l'exportateur.
// (Le certificat PDF est aussi autorisé pour son rôle.)
export function ControllerLotDetail() {
  return <LotDetailPage />
}
