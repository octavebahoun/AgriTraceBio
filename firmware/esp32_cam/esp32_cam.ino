// AgriTraceBio — Firmware ESP32-CAM (AI-Thinker OV2640)
// Expose /capture (JPEG unique) et /stream (MJPEG) sur le WiFi local.
// Le Raspberry Pi vient chercher les images pour analyse YOLO.
#include "config.h"
#include "Camera.h"
#include "CameraServer.h"
#include "WifiManager.h"

Camera        camera;
CameraServer  server;
WifiManager   wifi;

static void blink(uint8_t pin, uint8_t n, unsigned long ms = 100) {
  for (uint8_t i = 0; i < n; ++i) {
    digitalWrite(pin, HIGH); delay(ms);
    digitalWrite(pin, LOW);  delay(ms);
  }
}

void setup() {
  Serial.begin(115200);
  delay(300);
  Serial.println("\n=== AgriTraceBio ESP32-CAM ===");

  pinMode(PIN_INDICATOR_LED, OUTPUT);

  if (!camera.begin()) {
    Serial.println("[fatal] caméra non détectée. redémarrage dans 5 s");
    delay(5000);
    ESP.restart();
  }

  if (!wifi.begin()) {
    Serial.println("[fatal] WiFi indispo. redémarrage dans 5 s");
    delay(5000);
    ESP.restart();
  }

  if (!server.begin(HTTP_PORT)) {
    Serial.println("[fatal] serveur HTTP KO. redémarrage");
    delay(2000);
    ESP.restart();
  }

  blink(PIN_INDICATOR_LED, 3);   // signal visuel : prêt
}

void loop() {
  // Le serveur HTTP tourne dans sa propre tâche : ici on surveille le WiFi.
  if (!wifi.isConnected()) {
    Serial.println("[wifi] perdu, redémarrage");
    delay(2000);
    ESP.restart();
  }
  delay(5000);
}
