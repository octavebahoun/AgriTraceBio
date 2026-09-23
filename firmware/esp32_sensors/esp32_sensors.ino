// AgriTraceBio — Firmware ESP32 capteurs
// Lit DS18B20 + MQ-3 + MQ-135 et envoie les mesures au backend via WiFi.
#include "config.h"
#include "Sensors.h"
#include "WifiManager.h"
#include "Uploader.h"

Sensors      sensors;
WifiManager  wifi;
Uploader     uploader;

static void blink(uint8_t n, unsigned long ms = 120) {
  for (uint8_t i = 0; i < n; ++i) {
    digitalWrite(PIN_LED, HIGH); delay(ms);
    digitalWrite(PIN_LED, LOW);  delay(ms);
  }
}

void setup() {
  Serial.begin(115200);
  delay(300);
  Serial.println("\n=== AgriTraceBio ESP32 capteurs ===");

  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);

  sensors.begin();
  wifi.begin();

  Serial.println("[boot] chauffe capteurs MQ...");
  delay(WARMUP_MS);
  Serial.println("[boot] prêt");
}

void loop() {
  SensorReading r = sensors.read();
  Serial.printf("[sensors] temp=%.2f°C  eth=%.0f ppm  air=%.0f ppm\n",
                r.temperature_c, r.ethanol_ppm, r.air_quality_ppm);

  if (wifi.ensureConnected()) {
    bool ok = uploader.post(r, CURRENT_LOT_ID, DEVICE_ID);
    blink(ok ? 1 : 3);
  } else {
    blink(5);
  }

  delay(READ_INTERVAL_MS);
}
