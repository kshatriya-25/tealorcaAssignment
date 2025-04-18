# OM VIGHNHARTAYE NAMO NAMAH :

import requests
import random
from datetime import datetime
import time

API_URL = "http://localhost:8000/ingest"
TOKEN = "secret123"

PARAMETERS = ["temperature", "humidity", "sox"]

def simulate_data():
    while True:
        parameter = random.choice(PARAMETERS)
        value = round(random.uniform(20.0, 100.0), 2)
        timestamp = datetime.utcnow().isoformat()

        payload = {
            "parameter": parameter,
            "value": value,
            "timestamp": timestamp
        }

        headers = {
            "Authorization": f"Bearer {TOKEN}"
        }

        response = requests.post(API_URL, json=payload, headers=headers)
        print(f"Sent: {payload} | Status: {response.status_code}, Response: {response.json()}")
        time.sleep(3)

if __name__ == "__main__":
    simulate_data()
