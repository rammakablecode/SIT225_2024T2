import time
import csv
from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID = "e3ebd00d-5ac3-4b0e-9eed-7edfd5b37744"
SECRET_KEY = "TU8Io!fPN308vsO1yYxS9e4mM"

# Callback function on sensor value change event
def on_temperature_changed(client, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    csv_data = f"{timestamp},{value}\n"
    
    with open("temperature_data.csv", "a") as file:
        file.write(csv_data)
        file.flush()
    print(f"Temperature Data logged: {csv_data.strip()}")

def on_humidity_changed(client, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    csv_data = f"{timestamp},{value}\n"
    
    with open("humidity_data.csv", "a") as file:
        file.write(csv_data)
        file.flush()
    print(f"Humidity Data logged: {csv_data.strip()}")

def main():
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    client.register("temperature", value=None, on_write=on_temperature_changed)
    client.register("humidity", value=None, on_write=on_humidity_changed)
    client.start()

if __name__ == "__main__":
    main()
