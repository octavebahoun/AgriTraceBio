"""Service de domaine : détecte les alertes à partir d'une mesure."""
from src.domain.entities.alert import Alert, AlertLevel, AlertType
from src.domain.entities.measurement import Measurement
from src.domain.services.thresholds import (
    AIR_QUALITY_MAX,
    ETHANOL_MAX,
    TEMPERATURE_MAX,
    TEMPERATURE_MIN,
    Threshold,
)


class AlertDetector:
    def detect(self, m: Measurement) -> list[Alert]:
        alerts: list[Alert] = []
        alerts.extend(self._check_temperature(m))
        alerts.extend(self._check_ethanol(m))
        alerts.extend(self._check_air_quality(m))
        return alerts

    def _check_temperature(self, m: Measurement) -> list[Alert]:
        alerts: list[Alert] = []
        if m.temperature <= TEMPERATURE_MIN.critical:
            alerts.append(self._make(m, AlertType.TEMPERATURE, AlertLevel.CRITICAL,
                m.temperature, TEMPERATURE_MIN.critical,
                f"Température trop basse: {m.temperature}°C (seuil {TEMPERATURE_MIN.critical}°C)"))
        elif m.temperature <= TEMPERATURE_MIN.warning:
            alerts.append(self._make(m, AlertType.TEMPERATURE, AlertLevel.WARNING,
                m.temperature, TEMPERATURE_MIN.warning,
                f"Température basse: {m.temperature}°C"))
        elif m.temperature >= TEMPERATURE_MAX.critical:
            alerts.append(self._make(m, AlertType.TEMPERATURE, AlertLevel.CRITICAL,
                m.temperature, TEMPERATURE_MAX.critical,
                f"Température trop élevée: {m.temperature}°C (seuil {TEMPERATURE_MAX.critical}°C)"))
        elif m.temperature >= TEMPERATURE_MAX.warning:
            alerts.append(self._make(m, AlertType.TEMPERATURE, AlertLevel.WARNING,
                m.temperature, TEMPERATURE_MAX.warning,
                f"Température élevée: {m.temperature}°C"))
        return alerts

    def _check_ethanol(self, m: Measurement) -> list[Alert]:
        return self._check_max(m, m.ethanol_ppm, ETHANOL_MAX, AlertType.ETHANOL,
                               "Éthanol (dégradation ananas)")

    def _check_air_quality(self, m: Measurement) -> list[Alert]:
        return self._check_max(m, m.air_quality_ppm, AIR_QUALITY_MAX,
                               AlertType.AIR_QUALITY, "Qualité de l'air dégradée")

    def _check_max(self, m: Measurement, value: float, th: Threshold,
                   atype: AlertType, label: str) -> list[Alert]:
        if value >= th.critical:
            return [self._make(m, atype, AlertLevel.CRITICAL, value, th.critical,
                               f"{label}: {value} ppm (critique)")]
        if value >= th.warning:
            return [self._make(m, atype, AlertLevel.WARNING, value, th.warning,
                               f"{label}: {value} ppm (alerte)")]
        return []

    def _make(self, m: Measurement, atype: AlertType, level: AlertLevel,
              value: float, threshold: float, msg: str) -> Alert:
        return Alert(
            lot_id=m.lot_id,
            alert_type=atype,
            level=level,
            message=msg,
            value=value,
            threshold=threshold,
        )
