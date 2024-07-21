#define BLUE_LED_PIN 2
#define YELLOW_LED_PIN 3
#define WHITE_LED_PIN 4

void setup() {
  pinMode(BLUE_LED_PIN, OUTPUT);
  pinMode(YELLOW_LED_PIN, OUTPUT);
  pinMode(WHITE_LED_PIN, OUTPUT);
}

void loop() {
  // Mavi LED'i yak
  digitalWrite(BLUE_LED_PIN, HIGH);
  delay(1000);
  digitalWrite(BLUE_LED_PIN, LOW);
  
  // Sarı LED'i yak
  digitalWrite(YELLOW_LED_PIN, HIGH);
  delay(1000);
  digitalWrite(YELLOW_LED_PIN, LOW);
  
  // Beyaz LED'i yak
  digitalWrite(WHITE_LED_PIN, HIGH);
  delay(1000);
  digitalWrite(WHITE_LED_PIN, LOW);
}
