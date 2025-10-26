int REDPIN = 13;
int YELLOWPIN = 12;
int GREENPIN = 11;

void setup() {
  pinMode(REDPIN, OUTPUT);
  pinMode(YELLOWPIN, OUTPUT);
  pinMode(GREENPIN, OUTPUT);
}

void loop() {
  // Red ON
  digitalWrite(REDPIN, HIGH);
  digitalWrite(YELLOWPIN, LOW);
  digitalWrite(GREENPIN, LOW);
  delay(2000);

  // Yellow ON
  digitalWrite(REDPIN, LOW);
  digitalWrite(YELLOWPIN, HIGH);
  digitalWrite(GREENPIN, LOW);
  delay(2000);

  // Green ON
  digitalWrite(REDPIN, LOW);
  digitalWrite(YELLOWPIN, LOW);
  digitalWrite(GREENPIN, HIGH);
  delay(2000);
}
