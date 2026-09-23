#include "CameraServer.h"
#include "esp_camera.h"

#define BOUNDARY "AgriTraceBioFrame"
static const char* STREAM_TYPE =
  "multipart/x-mixed-replace; boundary=" BOUNDARY;
static const char* PART_HEADER =
  "\r\n--" BOUNDARY "\r\nContent-Type: image/jpeg\r\n"
  "Content-Length: %u\r\n\r\n";

static esp_err_t capture_handler(httpd_req_t* req) {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) return httpd_resp_send_500(req);

  httpd_resp_set_type(req, "image/jpeg");
  httpd_resp_set_hdr(req, "Content-Disposition",
                    "inline; filename=capture.jpg");
  esp_err_t res = httpd_resp_send(req, (const char*)fb->buf, fb->len);
  esp_camera_fb_return(fb);
  return res;
}

static esp_err_t stream_handler(httpd_req_t* req) {
  esp_err_t res = httpd_resp_set_type(req, STREAM_TYPE);
  if (res != ESP_OK) return res;

  char header[64];
  while (true) {
    camera_fb_t* fb = esp_camera_fb_get();
    if (!fb) { res = ESP_FAIL; break; }
    size_t hlen = snprintf(header, sizeof(header), PART_HEADER, fb->len);
    if (httpd_resp_send_chunk(req, header, hlen) != ESP_OK ||
        httpd_resp_send_chunk(req, (const char*)fb->buf, fb->len) != ESP_OK) {
      esp_camera_fb_return(fb);
      res = ESP_FAIL;
      break;
    }
    esp_camera_fb_return(fb);
  }
  return res;
}

static esp_err_t health_handler(httpd_req_t* req) {
  httpd_resp_set_type(req, "application/json");
  return httpd_resp_send(req, "{\"status\":\"ok\"}", 15);
}

bool CameraServer::begin(uint16_t port) {
  httpd_config_t cfg = HTTPD_DEFAULT_CONFIG();
  cfg.server_port = port;
  cfg.ctrl_port   = port + 100;

  if (httpd_start(&handle_, &cfg) != ESP_OK) {
    Serial.println("[srv] httpd_start KO");
    return false;
  }
  httpd_uri_t capture = { "/capture", HTTP_GET, capture_handler, nullptr };
  httpd_uri_t stream  = { "/stream",  HTTP_GET, stream_handler,  nullptr };
  httpd_uri_t health  = { "/health",  HTTP_GET, health_handler,  nullptr };
  httpd_register_uri_handler(handle_, &capture);
  httpd_register_uri_handler(handle_, &stream);
  httpd_register_uri_handler(handle_, &health);
  Serial.printf("[srv] écoute sur :%u  (/capture, /stream, /health)\n", port);
  return true;
}

void CameraServer::stop() {
  if (handle_) { httpd_stop(handle_); handle_ = nullptr; }
}
