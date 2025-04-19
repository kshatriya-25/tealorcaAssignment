# OM VIGHNHARTAYE NAMO NAMAH :

import json
import os
import time
import threading
from datetime import datetime
from kafka import KafkaConsumer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.database.session import SessionLoacal
from app.modals.masters import SensorData


load_dotenv()




KAFKA_TOPIC = "sensor-data"
BOOTSTRAP_SERVERS = "localhost:9092"


sensor_buffer = []
buffer_lock = threading.Lock()


def consume_sensor_data():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id="batch-db-writer",
        auto_offset_reset="latest"
    )
    print(" Kafka consomer started...")

    for message in consumer:
        with buffer_lock:
            sensor_buffer.append(message.value)


def batch_writer():
    while True:
        time.sleep(5)  
        print(f" Writing batch at {datetime.utcnow().isoformat()}")

        with buffer_lock:
            batch = sensor_buffer.copy()
            sensor_buffer.clear()

        if not batch:
            print(" No data to write.")
            continue

        db: Session = SessionLoacal()
        try:
            entries = [
                SensorData(
                    parameter_id=item["parameter_id"],
                    value=item["value"],
                    time=datetime.fromisoformat(item["timestamp"])
                )
                for item in batch
            ]
            db.bulk_save_objects(entries)
            db.commit()
            print(f"Inserted {len(entries)} records to DB")
        except Exception as e:
            print(f" DB Write Error: {e}")
            db.rollback()
        finally:
            db.close()


if __name__ == "__main__":
    threading.Thread(target=consume_sensor_data, daemon=True).start()
    batch_writer()
