// Configuration matérielle et paramètres du firmware ESP32.
// Copier secrets.h.example en secrets.h et remplir les identifiants.
#pragma once
#include "secrets.h"

// ---- Broches capteurs ----
#define PIN_DS18B20     4     // OneWire (avec pull-up 4.7 kΩ vers 3V3)
#define PIN_MQ3         34    // ADC1_CH6 (éthanol)
#define PIN_MQ135       35    // ADC1_CH7 (qualité air / CO2 / NH3)
#define PIN_LED         2     // LED d'état intégrée

// ---- Cadence ----
#define READ_INTERVAL_MS      30000UL   // 30 s entre 2 lectures
#define WIFI_TIMEOUT_MS       15000UL
#define HTTP_TIMEOUT_MS       8000UL
#define WARMUP_MS             10000UL   // temps de chauffe capteurs MQ

// ---- Backend ----
// Identifie ce nœud dans le backend
#define DEVICE_ID       "esp32-truck-01"
// Code du lot en cours de transport (à mettre à jour selon le voyage)
#define CURRENT_LOT_ID  "AGR-001"

// ---- Calibration MQ (grossière) ----
// Les capteurs MQ sont non linéaires. Ces coefficients donnent un ordre de
// grandeur en ppm. À raffiner après calibration réelle avec un gaz témoin.
#define MQ_ADC_MAX      4095.0f
#define MQ_VREF         3.3f
#define MQ3_R0          10.0f   // résistance de référence à l'air propre
#define MQ135_R0        76.63f
#define MQ_RL           10.0f   // résistance de charge (kΩ)
