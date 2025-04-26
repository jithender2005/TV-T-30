#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <MFRC522.h>

// LCD setup
LiquidCrystal_I2C lcd(0x27, 16, 2);

// RFID setup
#define SS_PIN 10
#define RST_PIN 9
MFRC522 rfid(SS_PIN, RST_PIN);

// Student data structure
struct Student {
  String uid;
  String name;
  String roll;
};

// List of students
Student students[] = {
  {"A1CDBC89", "JITHENDER", "6213"},
  {"0479276AB76680", "PRATHIK", "6946"},
  {"A1BAF904", "MEGHANA", "6632"},
  {"046FC0E2AD1490", "VAISHNAVI", "6661"},
  {"04891AE2AD1490", "JASHWANTH", "6238"}
};

const int numStudents = sizeof(students) / sizeof(students[0]);
bool attendanceMarked[numStudents] = {false}; // Track attendance status

void setup() {
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Scan your card");
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial())
    return;

  String uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) uid += "0";
    uid += String(rfid.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();

  Serial.print("Scanned UID: ");
  Serial.println(uid);

  lcd.clear();

  bool found = false;
  for (int i = 0; i < numStudents; i++) {
    if (uid == students[i].uid) {
      found = true;
      if (!attendanceMarked[i]) {
        attendanceMarked[i] = true;
        lcd.setCursor(0, 0);
        lcd.print("Name: " + students[i].name);
        lcd.setCursor(0, 1);
        lcd.print("Roll: " + students[i].roll);
        Serial.println("Student: " + students[i].name + ", Roll: " + students[i].roll);
      } else {
        lcd.setCursor(0, 0);
        lcd.print(students[i].name);
        lcd.setCursor(0, 1);
        lcd.print("Already marked");
        Serial.println("Attendance already marked");
      }
      break;
    }
  }

  if (!found) {
    lcd.setCursor(0, 0);
    lcd.print("UID:");
    lcd.setCursor(0, 1);
    lcd.print(uid);
    Serial.println("Unknown card");
  }

  delay(3000); // Show info for 3 seconds
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Scan your card");
}
