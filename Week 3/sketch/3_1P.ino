#include "thingProperties.h"
#include "DHT.h"

#define DHTPIN 2  // DHT11 data pin connected to Arduino Pin 2
#define DHTTYPE DHT11  // DHT 11 sensor type

DHT dht(DHTPIN, DHTTYPE);  // Create DHT object

// Function to handle changes in humidity
void onHumidityChange() {
  Serial.println("Humidity value changed in the cloud");
}

// Function to handle changes in temperature
void onTemperatureChange() {
  Serial.println("Temperature value changed in the cloud");
}

void setup() {
  // Initialize serial communication for debugging
  Serial.begin(9600);

  // Initialize the DHT sensor
  dht.begin();

  // This delay gives the chance to wait for a Serial Monitor without blocking if none is found
  delay(1500); 

  // Initialize Arduino IoT Cloud properties (defined in thingProperties.h)
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  // Set the level of debugging information
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  // Update Arduino Cloud with sensor values
  ArduinoCloud.update();

  // Read temperature and humidity values from the DHT11 sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Check if the readings are valid
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Assign sensor values to cloud variables
  temperature = temperature;
  humidity = humidity;

  // Print values to Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C, Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  // Wait for 5 seconds before taking the next reading
  delay(5000);
}
