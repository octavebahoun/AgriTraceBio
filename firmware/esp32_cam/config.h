// Configuration ESP32-CAM AI-Thinker.
#pragma once
#include "secrets.h"

// LED flash intégrée (GPIO 4). Attention : partagée avec la carte SD.
#define PIN_FLASH_LED     4
#define PIN_INDICATOR_LED 33   // LED rouge inversée sur la face arrière

// Qualité d'image (voir sensor.h : PIXFORMAT_JPEG, framesize_t)
#define IMG_FRAMESIZE     FRAMESIZE_VGA   // 640x480, bon compromis pour YOLO
#define IMG_JPEG_QUALITY  12               // 0 (best) .. 63 (worst)
#define IMG_FB_COUNT      2                // double buffer si PSRAM

// Ne pas modifier : brochage AI-Thinker (OV2640).
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

#define WIFI_TIMEOUT_MS   15000UL
