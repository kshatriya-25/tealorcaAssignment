#OM VIGHNHARTAYE NAMO NAMAH


import asyncio
from fastapi import APIRouter, WebSocket
from kafka import KafkaConsumer
import threading
import json

router = APIRouter()
KAFKA_TOPIC = "sensor-data"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

clients = set()

@router.websocket("/ws/sensor-stream")
async def sensor_websocket(websocket : WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except Exception:
        pass
    finally:
        clients.remove(websocket)

def kafka_listener():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id="sensor-group",
        auto_offset_reset="latest"
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def broadcast(message):
        dead_clients = []
        for client in clients:
            try:
                await client.send_json(message)
            except:
                dead_clients.append(client)
        for dc in dead_clients:
            clients.remove(dc)

    for msg in consumer:
        loop.run_until_complete(broadcast(msg.value))


threading.Thread(target=kafka_listener, daemon=True).start()