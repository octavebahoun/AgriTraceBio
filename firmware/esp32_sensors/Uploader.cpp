#include "Uploader.h"
#include "config.h"
#include <HTTPClient.h>
#include <ArduinoJson.h>

bool Uploader::post(const SensorReading& r,
                    const char* lot_id, const char* device_id) {
  HTTPClient http;
  String url = String(BACKEND_URL) + "/api/measurements";
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(HTTP_TIMEOUT_MS);

  StaticJsonDocument<256> doc;
  doc["lot_id"]           = lot_id;
  doc["device_id"]        = device_id;
  doc["temperature"]      = isnan(r.temperature_c) ? 0.0f : r.temperature_c;
  doc["ethanol_ppm"]      = r.ethanol_ppm;
  doc["air_quality_ppm"]  = r.air_quality_ppm;

  String payload;
  serializeJson(doc, payload);

  Serial.print("[http] POST ");
  Serial.print(url);
  Serial.print(" ← ");
  Serial.println(payload);

  int code = http.POST(payload);
  if (code > 0) {
    Serial.print("[http] réponse ");
    Serial.println(code);
  } else {
    Serial.print("[http] erreur ");
    Serial.println(http.errorToString(code));
  }
  http.end();
  return code >= 200 && code < 300;
}
