#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int ledPin = 7;
const int buzzerPin = 6;
LiquidCrystal_I2C lcd(0x27, 16, 2);

String receivedString = "";

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
  lcd.begin();
  lcd.backlight();
  lcd.clear();
}

void loop() {
  if (Serial.available()) {
    char receivedChar = Serial.read();
    if (receivedChar == '\n') {
      if (receivedString != "0") {
        digitalWrite(ledPin, HIGH);
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Tehlikeli Nesne:");
        lcd.setCursor(0, 1);
        lcd.print(receivedString);

        for (int i = 0; i < 3; i++) {
          digitalWrite(buzzerPin, HIGH);
          delay(1500);
          digitalWrite(buzzerPin, LOW);
          delay(500);
        }
        digitalWrite(ledPin, LOW);
        lcd.clear();
      }
      receivedString = "";
    } else {
      receivedString += receivedChar;
    }
  }
}
