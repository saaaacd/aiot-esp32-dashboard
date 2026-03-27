import requests
import time
import random
import json

FLASK_URL = "http://127.0.0.1:5000/sensor"

def generate_sensor_data():
    return {
        "temp": round(random.uniform(20.0, 35.0), 2),
        "humid": round(random.uniform(40.0, 80.0), 2),
        "metadata": json.dumps({
            "device_id": "ESP32_WiFi_Link",
            "rssi": random.randint(-80, -40),
            "ip": "192.168.1.100"
        })
    }

def main():
    print("Starting ESP32 Simulator...")
    while True:
        data = generate_sensor_data()
        try:
            response = requests.post(FLASK_URL, json=data)
            print(f"[{time.strftime('%H:%M:%S')}] Sent: {data} -> Status: {response.status_code}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Connection error: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()
