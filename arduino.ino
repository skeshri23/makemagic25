// Pin definitions
int greenPin = 2; // Green LED pin
int yellowPin = 3; // Yellow LED pin
int redPin = 4; // Red LED pin
int buzzerPin = 5; // Buzzer pin (for distress)

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set pins as OUTPUT
  pinMode(greenPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  // Ensure all LEDs and buzzer are off at the start
  digitalWrite(greenPin, LOW);
  digitalWrite(yellowPin, LOW);
  digitalWrite(redPin, LOW);
  digitalWrite(buzzerPin, LOW);
}

void loop() {
  // Check if data is available from the Raspberry Pi
  if (Serial.available() > 0) {
    // Read the data sent from the Raspberry Pi
    String soundType = Serial.readStringUntil('\n'); // Read until newline

    // Control the LEDs and buzzer based on the sound type received
    if (soundType == "green") {
      // Green sound detected (Normal)
      digitalWrite(greenPin, HIGH);
      digitalWrite(yellowPin, LOW);
      digitalWrite(redPin, LOW);
      digitalWrite(buzzerPin, LOW);
    } 
    else if (soundType == "yellow") {
      // Yellow sound detected (Suspicious)
      digitalWrite(greenPin, LOW);
      digitalWrite(yellowPin, HIGH);
      digitalWrite(redPin, LOW);
      digitalWrite(buzzerPin, LOW);
    } 
    else if (soundType == "red") {
      // Red sound detected (Distress)
      digitalWrite(greenPin, LOW);
      digitalWrite(yellowPin, LOW);
      digitalWrite(redPin, HIGH);
      digitalWrite(buzzerPin, HIGH); // Turn on buzzer for distress
    }
    delay(1000); // Wait for 1 second before checking again
  }
}
