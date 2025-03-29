#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino.h>

// Replace with your network credentials
const char* ssid = "WIFI@OSU";
const char* password = "";

// Replace with your server's IP or API endpoint
const String serverUrl = "https://xdewqotingvjamnlopfd.supabase.co"; // Example URL

void setup() {
  // Start serial communication
  Serial.begin(115200);
  delay(1000);

  // Connect to Wi-Fi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Optionally, print out the IP address
  Serial.println(WiFi.localIP());
}

void loop() {
  // Check if the Raspberry Pi has sent a classification (e.g., distress sound)
  if (Serial.available() > 0) {
    String soundType = Serial.readStringUntil('\n'); // Read until newline

    if (soundType == "red") {
      // If distress (red) sound is detected, send an alert to cloud service
      sendAlertToCloud();
    }

    delay(1000); // Wait a second before checking again
  }
}

void sendAlertToCloud() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Specify the server URL
    http.begin(serverUrl);

    // Specify HTTP headers (e.g., Content-Type for JSON)
    http.addHeader("Content-Type", "application/json");

    // Create JSON payload for the alert
    String payload = "{\"alert\": \"Distress sound detected\", \"device\": \"ESP32\", \"timestamp\": \"" + String(millis()) + "\"}";

    // Send HTTP POST request with the payload
    int httpResponseCode = http.POST(payload);

    // Check the response code
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Response: " + response);
    } else {
      Serial.println("Error sending alert: " + String(httpResponseCode));
    }

    // End the HTTP request
    http.end();
  } else {
    Serial.println("WiFi not connected!");
  }
}
