import serial
import time
import json
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase with the correct credentials
cred_obj = firebase_admin.credentials.Certificate(
    r'C:\Users\ramma\Downloads\sit225-5-firebase-adminsdk-o982n-f4f8bea959.json'
)
firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://sit225-5-default-rtdb.firebaseio.com//'
})

# Set up Serial communication
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Allow some time for Arduino to initialize

# Firebase database reference
ref = db.reference('mpu6050_data')

while True:
    data = ser.readline().decode('utf-8').strip()
    if data:
        try:
            # Parse the labeled data
            if "Gyro X:" in data:
                parts = data.replace("Gyro X: ", "").replace("Y: ", "").replace("Z: ", "").split(",")
                gyro_x, gyro_y, gyro_z = map(float, parts)
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                
                # Prepare data in JSON format
                gyro_data = {
                    "timestamp": timestamp,
                    "gyro_x": gyro_x,
                    "gyro_y": gyro_y,
                    "gyro_z": gyro_z
                }
                
                # Push data to Firebase
                ref.push(gyro_data)
                print(f"Data sent: {gyro_data}")
        except ValueError:
            print(f"Error parsing data: {data}")
    
    time.sleep(1)  # Adjust the data rate