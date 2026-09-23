# Orchestrateur edge — Raspberry Pi 4

Ce service tourne sur le Raspberry Pi 4 embarqué dans le camion. Il :

1. Récupère une image de la caméra **ESP32-CAM** (endpoint `/capture`).
2. Fait tourner **YOLO v8** localement pour détecter la maturité et les
   moisissures des ananas.
3. Envoie un rapport d'inspection (JSON + image) au backend
   AgriTraceBio (`POST /api/inspections`).

Le tout est répété toutes les `CAPTURE_INTERVAL_S` secondes.

## Installation sur Raspberry Pi 4

```bash
sudo apt update && sudo apt install -y python3-venv python3-pip \
                                       libatlas-base-dev libjpeg-dev
git clone <ce repo> agritrace
cd agritrace/raspberry_orchestrator
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Configuration

```bash
cp .env.example .env
# Éditer les URLs, DEVICE_ID, CURRENT_LOT_CODE.
```

Placer les fichiers modèles YOLO dans `models/`. Deux modèles distincts
sont chargés (maturité et moisissures) — chacun peut être absent, le
service tournera sur ceux disponibles.

## Lancement manuel

```bash
.venv/bin/python main.py
```

## Démarrage automatique (systemd)

```bash
sudo cp systemd/agritrace-orchestrator.service /etc/systemd/system/
sudo systemctl enable --now agritrace-orchestrator
sudo journalctl -u agritrace-orchestrator -f
```

## Test hors ligne (sans caméra ni Pi)

```bash
.venv/bin/python -m pytest tests/ -v
```

## Notes

- Les modèles YOLO doivent être des `.pt` compatibles Ultralytics.
- L'inférence CPU sur Pi 4 est lente (~1–2 s / image, VGA) — c'est
  suffisant pour l'intervalle par défaut de 60 s.
- Pour accélérer, exporter le modèle vers **NCNN** ou **ONNX** :
  `yolo export model=… format=ncnn`.
