import requests
import random
import time
import json

# Configuration
API_ENDPOINT = "http://backend:5000/data"
DEVICE_ID = "ESP32_FACTORY_001"
SENSOR_TYPES = ["TEMPERATURE", "HUMIDITY", "VIBRATION", "PRESSURE"]

def generate_sensor_data():
    """Generate simulated industrial sensor data"""
    return {
        "device_id": DEVICE_ID,
        "timestamp": int(time.time()),
        "readings": {
            "TEMPERATURE": round(random.uniform(20.0, 45.0), 1),
            "HUMIDITY": round(random.uniform(30.0, 85.0), 1),
            "VIBRATION": round(random.uniform(0.1, 2.5), 2),
            "PRESSURE": round(random.uniform(100.0, 150.0), 1)
        },
        "status": random.choice(["NORMAL", "WARNING", "CRITICAL"])
    }

def send_to_backend(data):
    """Send data to cloud backend"""
    try:
        response = requests.post(
            API_ENDPOINT,
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Data sent. Status: {response.status_code}")
    except Exception as e:
        print(f"Transmission error: {str(e)}")

if __name__ == "__main__":
    print("Starting Industrial IoT Device Simulator...")
    while True:
        sensor_data = generate_sensor_data()
        print(f"Generated: {json.dumps(sensor_data, indent=2)}")
        send_to_backend(sensor_data)
        time.sleep(15)  # Send every 15 seconds
