#include "WifiManager.h"
#include "config.h"
#include <WiFi.h>

bool WifiManager::begin() {
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);           // meilleure réactivité pour le stream
  WiFi.setAutoReconnect(true);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("[wifi] connexion");
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
  Serial.println("[wifi] échec au boot");
  return false;
}

bool WifiManager::isConnected() const {
  return WiFi.status() == WL_CONNECTED;
}
