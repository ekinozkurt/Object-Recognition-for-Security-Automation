#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

// LED pin tanımlamaları
#define BLUE_LED_PIN 2
#define YELLOW_LED_PIN 3
#define WHITE_LED_PIN 4

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("RFID modülü hazır.");

  // LED pin modlarını ayarla
  pinMode(BLUE_LED_PIN, OUTPUT);
  pinMode(YELLOW_LED_PIN, OUTPUT);
  pinMode(WHITE_LED_PIN, OUTPUT);

  // Başlangıçta beyaz LED'i yak
  digitalWrite(BLUE_LED_PIN, LOW);
  digitalWrite(YELLOW_LED_PIN, LOW);
  digitalWrite(WHITE_LED_PIN, HIGH);
}

void loop() {
  // Seriden gelen veri kontrolü
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "close") {
      // Tüm LED'leri kapat
      digitalWrite(BLUE_LED_PIN, LOW);
      digitalWrite(YELLOW_LED_PIN, LOW);
      digitalWrite(WHITE_LED_PIN, LOW);
      return;
    }
  }

  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    uid += String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    uid += String(mfrc522.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();
  uid.trim();
  Serial.println(uid);

  if (uid == "13 35 D6 83") {
    Serial.println("start_ui");
    digitalWrite(BLUE_LED_PIN, HIGH);
    digitalWrite(YELLOW_LED_PIN, LOW);
    digitalWrite(WHITE_LED_PIN, LOW);
  } else if (uid == "D2 06 EB 1B") {
    Serial.println("stop_ui");
    digitalWrite(BLUE_LED_PIN, LOW);
    digitalWrite(YELLOW_LED_PIN, HIGH);
    digitalWrite(WHITE_LED_PIN, LOW);
  } else {
    digitalWrite(BLUE_LED_PIN, LOW);
    digitalWrite(YELLOW_LED_PIN, LOW);
    digitalWrite(WHITE_LED_PIN, HIGH);
  }

  mfrc522.PICC_HaltA();
}
