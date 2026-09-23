// Connexion WiFi bloquante (au boot uniquement — le serveur HTTP a besoin
// d'un lien stable dès le démarrage).
#pragma once
#include <Arduino.h>

class WifiManager {
 public:
  bool begin();     // renvoie true si connecté avant WIFI_TIMEOUT_MS
  bool isConnected() const;
};
