#include "Sensors.h"
#include "config.h"
#include <OneWire.h>
#include <DallasTemperature.h>

static OneWire oneWire(PIN_DS18B20);
static DallasTemperature dallas(&oneWire);

void Sensors::begin() {
  dallas.begin();
  dallas.setResolution(11);         // 0.125°C, ~375 ms
  analogReadResolution(12);         // 0..4095
  analogSetPinAttenuation(PIN_MQ3, ADC_11db);
  analogSetPinAttenuation(PIN_MQ135, ADC_11db);
}

SensorReading Sensors::read() {
  SensorReading r;
  r.temperature_c   = readTemperatureC();
  r.ethanol_ppm     = readMq3Ppm();
  r.air_quality_ppm = readMq135Ppm();
  return r;
}

float Sensors::readTemperatureC() {
  dallas.requestTemperatures();
  float t = dallas.getTempCByIndex(0);
  if (t == DEVICE_DISCONNECTED_C || t < -40 || t > 100) return NAN;
  return t;
}

float Sensors::readMq3Ppm() {
  return voltageToPpm(adcToVoltage(analogRead(PIN_MQ3)), MQ3_R0);
}

float Sensors::readMq135Ppm() {
  return voltageToPpm(adcToVoltage(analogRead(PIN_MQ135)), MQ135_R0);
}

float Sensors::adcToVoltage(int raw) {
  return (float)raw * (MQ_VREF / MQ_ADC_MAX);
}

// Conversion approximative Rs/R0 → ppm (courbe simplifiée log-log).
// Formule : ppm ≈ a * (Rs/R0)^b   avec a, b tirés des datasheets MQ.
float Sensors::voltageToPpm(float voltage, float r0) {
  if (voltage < 0.01f) return 0.0f;
  float rs = MQ_RL * (MQ_VREF - voltage) / voltage;
  float ratio = rs / r0;
  const float a = 116.6020682f;
  const float b = -2.769034857f;
  float ppm = a * pow(ratio, b);
  if (isnan(ppm) || ppm < 0) return 0.0f;
  if (ppm > 10000) return 10000;
  return ppm;
}
