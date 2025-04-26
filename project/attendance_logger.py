import serial
from db import create_db, log_attendance

students = {
    "A1BAF904": ("MEGHANA", "6632"),
    "0479276AB76680": ("PRATHIK", "6946"),
    "046FC0E2AD1490": ("VAISHNAVI", "6661"),
    "A1CDBC89": ("JITHENDER", "6213"),
    "04891AE2AD1490": ("JASHWANTH", "6238")
}

create_db()

ser = serial.Serial('COM3', 9600)
print("Listening for RFID scans...")

while True:
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        if "Scanned UID:" in line:
            uid = line.split(":")[-1].strip()
            if uid in students:
                name, roll = students[uid]
                if log_attendance(uid, name, roll):
                    print(f"Marked: {name} ({roll})")
                else:
                    print(f"Already marked today: {name}")
            else:
                print(f"Unknown UID: {uid}")