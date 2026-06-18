void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT); // Using built-in LED as test
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    
    if (data == '1') {
      digitalWrite(13, HIGH); // Turn on hardware
      delay(1000);            // Keep it on for 1 second
      digitalWrite(13, LOW);  // Turn off
    }
  }
}
