// Lecture des trois capteurs et calcul des grandeurs physiques.
#pragma once
#include <Arduino.h>

struct SensorReading {
  float temperature_c;   // °C, NAN si lecture invalide
  float ethanol_ppm;
  float air_quality_ppm;
};

class Sensors {
 public:
  void begin();
  SensorReading read();
 private:
  float readTemperatureC();
  float readMq3Ppm();
  float readMq135Ppm();
  float adcToVoltage(int raw);
  float voltageToPpm(float voltage, float r0);
};
