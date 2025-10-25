#include <Servo.h>

Servo myServo;
const int SERVO_PIN = 9;    // Подключи SG-5010 к пину 9
const int OPEN_ANGLE = 90;  // Угол открытия
const int CLOSED_ANGLE = 0; // Исходное положение

void setup() {
  Serial.begin(9600);
  myServo.attach(SERVO_PIN);
  myServo.write(CLOSED_ANGLE);  // Изначально закрыт
  Serial.println("Arduino готово ✅");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "OPEN") {
      Serial.println("📩 Команда: OPEN → открываю");
      myServo.write(OPEN_ANGLE);
      delay(10000); // держим открытым 10 секунд
      Serial.println("↩️ Закрываю");
      myServo.write(CLOSED_ANGLE);
    } 
    else if (command == "DENY") {
      Serial.println("📩 Команда: DENY → доступ запрещён");
      // Ничего не делаем, просто лог
    }
  }
}