# AgriTraceBio

Système de traçabilité **IoT + IA + Blockchain** pour la filière ananas au
Bénin. Suit chaque lot depuis la récolte jusqu'au consommateur final,
détecte automatiquement les anomalies de transport et garantit l'intégrité
des données.

## Architecture

```
┌────────────────────┐     WiFi     ┌────────────────────┐
│  ESP32 + capteurs  │─────HTTP────▶│                    │
│  (temp, gaz, air)  │              │   Backend Flask    │
└────────────────────┘              │   + MongoDB        │
                                    │   + Blockchain     │◀── Frontend
┌────────────────────┐              │   + Certificats    │    Vite/React
│    ESP32-CAM       │◀── pull ────▶│                    │
│   (OV2640 JPEG)    │              └────────────────────┘
└────────────────────┘                        ▲
         ▲                                    │
         │ /capture                           │
         ▼                                    │
┌────────────────────┐                        │
│  Raspberry Pi 4    │──── YOLO ─────POST────┘
│  (orchestrateur)   │
└────────────────────┘
```

## Contenu du dépôt

| Dossier                    | Rôle                                         |
| -------------------------- | -------------------------------------------- |
| `backend/`                 | API Flask + Mongo + blockchain interne + PDF |
| `frontend/`                | Vite + React + Tailwind, 3 interfaces        |
| `firmware/esp32_sensors/`  | Firmware Arduino : DS18B20 + MQ-3 + MQ-135   |
| `firmware/esp32_cam/`      | Firmware ESP32-CAM : serveur HTTP JPEG/MJPEG |
| `raspberry_orchestrator/`  | Service Python : capture → YOLO → backend    |
| `docker-compose.yml`       | Backend + MongoDB en un seul `up`            |

## Démarrage rapide (backend + mongo)

```bash
cp .env.example .env      # éditer JWT_SECRET
docker compose up -d --build
curl http://localhost:5000/api/health
```

## Démarrage du frontend

```bash
cd frontend
npm install
npm run dev               # http://localhost:5173
```

## Comptes de test

Le backend ne pré-crée aucun compte. Créer un exportateur :

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"exp@agritrace.bj","password":"password123",
       "name":"Exportateur","role":"exporter"}'
```

Rôles : `admin`, `exporter`, `controller`. Consommateur = pas de compte
(page publique via QR code).

## Firmwares embarqués

Chaque dossier `firmware/*` contient son propre `README.md` avec câblage
et configuration. Copier `secrets.h.example` → `secrets.h` et renseigner
le WiFi + l'URL du backend avant flash.

## Raspberry Pi (edge orchestrateur)

Voir `raspberry_orchestrator/README.md`. Installe une venv Python, tire les
images de l'ESP32-CAM, exécute YOLO localement et POST les rapports vers
`/api/inspections`.

## Endpoints principaux

| Méthode | Chemin                                     | Description               |
| ------- | ------------------------------------------ | ------------------------- |
| POST    | `/api/auth/register` / `/login`            | Création / connexion      |
| GET     | `/api/lots` (+ CRUD)                       | Lots d'ananas             |
| POST    | `/api/measurements`                        | Mesure IoT + alertes auto |
| POST    | `/api/inspections` (multipart)             | Rapport YOLO + image      |
| GET     | `/api/alerts/active`                       | Alertes ouvertes          |
| GET     | `/api/blockchain/verify`                   | Vérifie l'intégrité       |
| GET     | `/api/lots/code/<code>/qr.svg`             | QR code d'un lot          |
| GET     | `/api/certificates/lot/<code>.pdf`         | Certificat PDF            |
| GET     | `/api/public/trace/<code>`                 | Traçabilité publique      |

## Auteurs

ADOOUNWA Nelson Mandela & CHADARE Steaven Ibitayo K.  
Superviseur : Dr KONNON M. Abel — INSTI Lokossa, UNSTIM (Bénin).  
Année académique 2025–2026.
