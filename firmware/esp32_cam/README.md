# Firmware ESP32-CAM — Vision embarquée

Carte visée : **AI-Thinker ESP32-CAM** (OV2640 + 4 Mo PSRAM).

Après démarrage, la carte se connecte au WiFi et démarre un serveur HTTP
qui expose trois routes que le Raspberry Pi peut interroger :

| Route      | Méthode | Réponse                              |
| ---------- | ------- | ------------------------------------ |
| `/capture` | GET     | Image JPEG unique (640×480)          |
| `/stream`  | GET     | Flux MJPEG (multipart/x-mixed-replace) |
| `/health`  | GET     | `{"status":"ok"}`                   |

## Câblage flashing

L'ESP32-CAM n'a pas d'USB : il faut un adaptateur **FTDI USB-série**.

| FTDI    | ESP32-CAM |
| ------- | --------- |
| 5V      | 5V        |
| GND     | GND       |
| TX      | U0R (GPIO 3) |
| RX      | U0T (GPIO 1) |
| GND     | IO0 (mise en mode flash) |

Après flash, débrancher IO0 ↔ GND puis appuyer sur RESET.

## Bibliothèques

- Core `esp32` (Espressif) — inclut `esp_camera.h` et `esp_http_server.h`
- Aucune lib externe supplémentaire

## Configuration

1. Copier `secrets.h.example` → `secrets.h`.
2. Renseigner `WIFI_SSID`, `WIFI_PASSWORD`.
3. Sélectionner la carte **AI Thinker ESP32-CAM** dans l'IDE Arduino.
4. Choisir un partitionnement **Huge APP (3MB No OTA)**.
5. Téléverser.

## Test rapide

Après boot, le moniteur série affiche l'IP obtenue. Depuis n'importe quel
navigateur :

```
http://<IP-ESP32CAM>/capture   → télécharge une photo
http://<IP-ESP32CAM>/stream    → affiche le flux vidéo
http://<IP-ESP32CAM>/health    → réponse JSON
```

C'est cette IP que l'orchestrateur Raspberry Pi utilisera pour tirer les
images à envoyer au modèle YOLO.
