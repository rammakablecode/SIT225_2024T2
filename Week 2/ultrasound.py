import serial
import time
import csv

# Setup the serial connection (adjust COM port as necessary)
arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)  # Allow time for Arduino to initialize

# Open a CSV file to store the data
with open('distance_data1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Distance"])  # CSV headers

    while True:
        data = arduino.readline().decode('utf-8').strip()  # Read from Arduino
        if data:
            timestamp = time.strftime("%Y%m%d%H%M%S")  # Timestamp in required format
            writer.writerow([timestamp, data])  # Save to CSV
            print(f"{timestamp}, {data}")  # Print data for debugging
        time.sleep(1)  # Adjust frequency if needed
