// Initialisation du capteur OV2640 embarqué sur la carte ESP32-CAM.
#pragma once
#include <Arduino.h>

class Camera {
 public:
  // Retourne true si l'initialisation a réussi.
  bool begin();
};
