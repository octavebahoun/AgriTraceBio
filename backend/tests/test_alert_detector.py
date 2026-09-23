"""Tests unitaires du détecteur d'alertes (pas besoin de Mongo)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.domain.entities.alert import AlertLevel, AlertType
from src.domain.entities.measurement import Measurement
from src.domain.services.alert_detector import AlertDetector


def make(temp=8.0, eth=10.0, air=200.0) -> Measurement:
    return Measurement(
        lot_id="L1", temperature=temp, ethanol_ppm=eth,
        air_quality_ppm=air, device_id="D1",
    )


def test_ok_no_alert():
    assert AlertDetector().detect(make()) == []


def test_temp_too_high_critical():
    alerts = AlertDetector().detect(make(temp=15.0))
    assert len(alerts) == 1
    assert alerts[0].alert_type == AlertType.TEMPERATURE
    assert alerts[0].level == AlertLevel.CRITICAL


def test_temp_high_warning():
    alerts = AlertDetector().detect(make(temp=11.0))
    assert alerts[0].level == AlertLevel.WARNING


def test_temp_too_low_critical():
    alerts = AlertDetector().detect(make(temp=3.0))
    assert alerts[0].level == AlertLevel.CRITICAL


def test_ethanol_critical():
    alerts = AlertDetector().detect(make(eth=250.0))
    assert alerts[0].alert_type == AlertType.ETHANOL
    assert alerts[0].level == AlertLevel.CRITICAL


def test_air_quality_warning():
    alerts = AlertDetector().detect(make(air=1200.0))
    assert alerts[0].alert_type == AlertType.AIR_QUALITY
    assert alerts[0].level == AlertLevel.WARNING


def test_multiple_alerts():
    alerts = AlertDetector().detect(make(temp=15.0, eth=250.0))
    assert len(alerts) == 2


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        try:
            t()
            print(f"OK   {t.__name__}")
        except AssertionError as e:
            print(f"FAIL {t.__name__}: {e}")
