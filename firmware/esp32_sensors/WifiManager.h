// Connexion WiFi non bloquante avec reconnexion automatique.
#pragma once
#include <Arduino.h>

class WifiManager {
 public:
  void begin();
  bool ensureConnected();     // renvoie true si WiFi.status() == WL_CONNECTED
  bool isConnected() const;
};
