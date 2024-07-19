import serial
import time
import random
from datetime import datetime
# Set up the serial port connection
baud_rate = 9600
serial_port = 'COM3'
s = serial.Serial(serial_port, baud_rate, timeout=5)
def log_event(event):
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"{timestamp} - {event}")
while True:
# Generate a random number between 1 and 10
num_blinks = random.randint(1, 10)
# Send the number to the Arduino
s.write(bytes(f"{num_blinks}\n", 'utf-8'))
log_event(f"Send >>> {num_blinks}")
# Wait for the Arduino to respond
response = s.readline().decode('utf-8').strip()
if response:
log_event(f"Recv <<< {response}")
delay_seconds = int(response)
# Wait for the specified number of seconds
log_event(f"Sleeping for {delay_seconds} seconds")
time.sleep(delay_seconds)
log_event(f"Done sleeping for {delay_seconds} seconds")
