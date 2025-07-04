#include <WiFi.h>
#include <WebSocketsClient.h>

// 🔹 WiFi Credentials
const char* ssid = "Test";
const char* password = "12345678";

// 🔹 WebSocket Client (ESP32 → ESP32 #2)
WebSocketsClient webSocket;

String incomingCommand = "";

// ===== Setup =====
void setup() {
  Serial.begin(115200);

  // 🔹 Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\n✅ ESP32 #1 WiFi Connected");

  // 🔹 Connect to ESP32 #2 WebSocket Server
  webSocket.begin("192.168.242.167", 81, "/");  // Replace with ESP32 #2 IP if not AP mode
  webSocket.onEvent(webSocketEvent);
}

// Optional WebSocket Event Handler
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  if (type == WStype_CONNECTED) {
    Serial.println("✅ Connected to ESP32 #2 via WebSocket");
  }
}

// ===== Loop =====
void loop() {
  webSocket.loop();

  while (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n') {
      incomingCommand.trim();
      Serial.println("📨 Sending: " + incomingCommand);
      webSocket.sendTXT(incomingCommand);
      incomingCommand = "";
    } else {
      incomingCommand += ch;
    }
  }
}
