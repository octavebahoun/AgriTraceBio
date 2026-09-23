#include "Camera.h"
#include "config.h"
#include "esp_camera.h"

bool Camera::begin() {
  camera_config_t cfg;
  cfg.ledc_channel = LEDC_CHANNEL_0;
  cfg.ledc_timer   = LEDC_TIMER_0;
  cfg.pin_d0 = Y2_GPIO_NUM;
  cfg.pin_d1 = Y3_GPIO_NUM;
  cfg.pin_d2 = Y4_GPIO_NUM;
  cfg.pin_d3 = Y5_GPIO_NUM;
  cfg.pin_d4 = Y6_GPIO_NUM;
  cfg.pin_d5 = Y7_GPIO_NUM;
  cfg.pin_d6 = Y8_GPIO_NUM;
  cfg.pin_d7 = Y9_GPIO_NUM;
  cfg.pin_xclk = XCLK_GPIO_NUM;
  cfg.pin_pclk = PCLK_GPIO_NUM;
  cfg.pin_vsync = VSYNC_GPIO_NUM;
  cfg.pin_href = HREF_GPIO_NUM;
  cfg.pin_sscb_sda = SIOD_GPIO_NUM;
  cfg.pin_sscb_scl = SIOC_GPIO_NUM;
  cfg.pin_pwdn = PWDN_GPIO_NUM;
  cfg.pin_reset = RESET_GPIO_NUM;
  cfg.xclk_freq_hz = 20000000;
  cfg.pixel_format = PIXFORMAT_JPEG;
  cfg.frame_size   = IMG_FRAMESIZE;
  cfg.jpeg_quality = IMG_JPEG_QUALITY;
  cfg.fb_count     = psramFound() ? IMG_FB_COUNT : 1;
  cfg.fb_location  = psramFound() ? CAMERA_FB_IN_PSRAM
                                  : CAMERA_FB_IN_DRAM;
  cfg.grab_mode    = CAMERA_GRAB_LATEST;

  esp_err_t err = esp_camera_init(&cfg);
  if (err != ESP_OK) {
    Serial.printf("[cam] init KO (0x%x)\n", err);
    return false;
  }
  Serial.println("[cam] OV2640 prêt");
  return true;
}
