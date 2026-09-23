# Firmware ESP32 — Capteurs environnementaux

Lit **DS18B20**, **MQ-3**, **MQ-135** et envoie les mesures au backend
AgriTraceBio par HTTP toutes les 30 s.

## Câblage

| Capteur / signal | Broche ESP32 | Notes                                    |
| ---------------- | ------------ | ---------------------------------------- |
| DS18B20 (data)   | GPIO 4       | Pull-up 4.7 kΩ entre data et 3V3         |
| MQ-3 AO          | GPIO 34      | ADC1 uniquement (WiFi utilise ADC2)      |
| MQ-135 AO        | GPIO 35      | ADC1 uniquement                          |
| LED d'état       | GPIO 2       | LED intégrée sur la plupart des cartes   |
| VCC capteurs     | 5V (Vin)     | Les MQ demandent 5V pour le chauffage    |
| GND commun       | GND          | À relier entre tous les modules          |

## Bibliothèques Arduino

À installer via le gestionnaire de bibliothèques :

- `OneWire`
- `DallasTemperature`
- `ArduinoJson` (v6.x)

Le core `esp32` de Espressif fournit `WiFi.h` et `HTTPClient.h`.

## Configuration

1. Copier `secrets.h.example` en `secrets.h`.
2. Remplir `WIFI_SSID`, `WIFI_PASSWORD`, `BACKEND_URL`.
3. Ouvrir `esp32_sensors.ino` dans l'IDE Arduino.
4. Sélectionner la carte "ESP32 Dev Module" et le port série.
5. Téléverser.

## Vérification

Ouvrir le moniteur série à **115200 baud**. À chaque cycle :

```
[sensors] temp=8.12°C  eth=42 ppm  air=310 ppm
[http] POST http://.../api/measurements ← {...}
[http] réponse 201
```

Une lecture réussie déclenche un flash court de la LED, une erreur WiFi
5 flashs rapides.

## Simulation sans matériel (Wokwi)

Un projet Wokwi équivalent peut être créé en assemblant :
`ESP32 DevKitC` + `DS18B20` + deux potentiomètres pour simuler MQ-3 / MQ-135.
