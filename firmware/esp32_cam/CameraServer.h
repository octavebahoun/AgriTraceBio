// Serveur HTTP embarqué : /capture (JPEG) + /stream (MJPEG) + /health.
#pragma once
#include <Arduino.h>
#include "esp_http_server.h"

class CameraServer {
 public:
  bool begin(uint16_t port);
  void stop();
 private:
  httpd_handle_t handle_ = nullptr;
};
