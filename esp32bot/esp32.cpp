#include <WiFi.h>
#include <WebServer.h>
#include <WiFiManager.h>

WebServer server(80);
int pins[] = {26, 25, 32, 33};

void handleRoot() {
  String html = "<!DOCTYPE html><html><head></head><body>";
  html += "<h4>"+ WiFi.SSID() + "</h4>";
  html += "<p>IP address: " + WiFi.localIP().toString() + "</p>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void handleControl() {
  if (server.hasArg("pins") && server.hasArg("state")) {
    String pinsArg = server.arg("pins");
    String state = server.arg("state");

    std::vector<int> pinNumbers;
    int start = 0;
    for (int i = 0; i <= pinsArg.length(); ++i) {
      if (i == pinsArg.length() || pinsArg[i] == ',') {
        pinNumbers.push_back(pinsArg.substring(start, i).toInt());
        start = i + 1;
      }
    }

    Serial.println("Received command for pins " + pinsArg + " to be set to " + state);

    for (int pinNumber : pinNumbers) {
      if (state == "high") {
        digitalWrite(pinNumber, HIGH);
        Serial.println("Pin " + String(pinNumber) + " set to HIGH");
      } else if (state == "low") {
        digitalWrite(pinNumber, LOW);
        Serial.println("Pin " + String(pinNumber) + " set to LOW");
      } else {
        server.send(400, "text/plain", "Invalid state");
        return;
      }
    }
    server.send(200, "text/plain", "Pins " + pinsArg + " set to " + state);
  } else {
    server.send(400, "text/plain", "Missing pins or state argument");
  }
}

void setup() {
  Serial.begin(115200);
  WiFiManager wifiManager;
  //wifiManager.resetSettings();
  wifiManager.setAPCallback([](WiFiManager* myWiFiManager) {
    Serial.println("Entered config mode");
    Serial.println(WiFi.softAPIP());
  });

  if (!wifiManager.autoConnect("ESP32-AP")) {
    Serial.println("Failed to connect and hit timeout");
    ESP.restart();
  }

  WiFi.mode(WIFI_AP_STA);
  Serial.println("Connected to WiFi");
  server.on("/", handleRoot);
  server.on("/control", handleControl);

  for (int i = 0; i < sizeof(pins) / sizeof(pins[0]); i++) {
    pinMode(pins[i], OUTPUT);
    digitalWrite(pins[i], LOW);
  }

  server.begin();
}

void loop() {
  server.handleClient();
}
