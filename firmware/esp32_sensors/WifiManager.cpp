#include "WifiManager.h"
#include "config.h"
#include <WiFi.h>

void WifiManager::begin() {
  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}

bool WifiManager::ensureConnected() {
  if (WiFi.status() == WL_CONNECTED) return true;

  Serial.print("[wifi] connexion");
  WiFi.disconnect();
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED &&
         millis() - start < WIFI_TIMEOUT_MS) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("[wifi] IP=");
    Serial.println(WiFi.localIP());
    return true;
  }
  Serial.println("[wifi] échec, nouvelle tentative au prochain cycle");
  return false;
}

bool WifiManager::isConnected() const {
  return WiFi.status() == WL_CONNECTED;
}
