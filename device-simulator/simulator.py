import random
import time
import requests
import yaml

class DeviceSimulator:
    def __init__(self, config_file):
        with open(config_file) as f:
            self.config = yaml.safe_load(f)
        
    def generate_payload(self, device):
        return {
            "device_id": device['id'],
            "temperature": round(random.uniform(20, 45), 1),
            "humidity": round(random.uniform(30, 85), 1),
            "vibration": round(random.uniform(0.1, 2.5), 2)
        }
    
    def run(self):
        while True:
            for device in self.config['devices']:
                try:
                    payload = self.generate_payload(device)
                    response = requests.post(
                        device['endpoint'],
                        json=payload,
                        timeout=5
                    )
                    print(f"{device['id']}: Sent (Status {response.status_code})")
                except Exception as e:
                    print(f"{device['id']}: Error - {str(e)}")
                
                time.sleep(device['interval'])

if __name__ == "__main__":
    simulator = DeviceSimulator("config.yaml")
    simulator.run()
