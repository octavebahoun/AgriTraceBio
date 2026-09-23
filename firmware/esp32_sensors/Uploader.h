// Envoi HTTP POST des mesures au backend AgriTraceBio.
#pragma once
#include <Arduino.h>
#include "Sensors.h"

class Uploader {
 public:
  // Retourne true si le backend a répondu 2xx.
  bool post(const SensorReading& r, const char* lot_id, const char* device_id);
};
