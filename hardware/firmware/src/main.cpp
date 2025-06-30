#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "sensors.h"

// Configuration
const char* SSID = "FactoryNET";
const char* PASSWORD = "securepass123";
const char* SERVER_URL = "http://backend:5000/api/v1/sensors";

DHT_Sensor dht(4, DHT22);  // GPIO4

void connectWiFi() {
  WiFi.begin(SSID, PASSWORD);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP: " + WiFi.localIP().toString());
}

void sendSensorData() {
  HTTPClient http;
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");
  
  String payload = String("{") +
    "\"device_id\":\"ESP32_01\"," +
    "\"temperature\":" + String(dht.readTemperature()) + "," +
    "\"humidity\":" + String(dht.readHumidity()) + "," +
    "\"vibration\":" + String(readVibration()) + 
  "}";

  int httpCode = http.POST(payload);
  http.end();
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  initVibrationSensor();
  connectWiFi();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    sendSensorData();
  }
  delay(30000);  // 30s interval
}
