#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>  // Make sure you have this library installed

// Your Wi-Fi credentials
const char* ssid = "WIFI@OSU";
const char* password = "";

// Supabase REST API URL
const char* supabaseUrl = "https://xdewqotingvjamnlopfd.supabase.co";
const char* apiKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhkZXdxb3Rpbmd2amFtbmxvcGZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMyNTQ5ODcsImV4cCI6MjA1ODgzMDk4N30.1XASDPP53GhvEWzOZtFyk-YLzr0CeePhu9mNVapimE0";  // Your Supabase Anon key

// Initialize Wi-Fi
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

// Send sensor data to Supabase
void sendToSupabase(float sensorValue) {
  HTTPClient http;
  http.begin(supabaseUrl);  // Begin HTTP request to Supabase
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + String(apiKey));

  // Create JSON payload
  StaticJsonDocument<200> doc;
  doc["sensor_value"] = sensorValue;  // Replace with actual sensor data
  String requestBody;
  serializeJson(doc, requestBody);

  // Send POST request to Supabase
  int httpCode = http.POST(requestBody);

  if (httpCode == 200) {
    Serial.println("Data successfully sent to Supabase");
  } else {
    Serial.print("Failed to send data. HTTP error code: ");
    Serial.println(httpCode);
  }

  http.end();  // End HTTP request
}

void loop() {
  // Example: Assume you're reading from an accelerometer or microphone here
  float sensorValue = analogRead(34);  // Change this to your actual sensor reading

  sendToSupabase(sensorValue);

  delay(5000);  // Send data every 5 seconds
}
