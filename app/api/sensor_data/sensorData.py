#OM VIGHNHARTAYE NAMO NAMAH :


from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from ...database.session import getdb
from ...modals.masters import SensorData, Parameter
from datetime import datetime
from pydantic import BaseModel
import logging
import kafka
router = APIRouter()
from kafka import KafkaProducer
import json

AUTH_TOKEN = "tealorca"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

KAFKA_TOPIC = "sensor-data"


class SensorIngestPayload(BaseModel):
    parameter: str
    value: float
    timestamp: datetime


@router.post("/ingest")
def ingest_data(
    payload: SensorIngestPayload,
    request: Request,
    db: Session = Depends(getdb)
):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid or missing token")

   
    param = db.query(Parameter).filter(Parameter.name == payload.parameter).first()
    if not param:
        raise HTTPException(status_code=404, detail="Parameter not found")

    
    message = {
        "parameter_id": param.id,
        "value": payload.value,
        "timestamp": payload.timestamp.isoformat()
    }

    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
    except Exception as e:
        logging.error(f"Kafka error: {e}")
        raise HTTPException(status_code=500, detail="Kafka error")

    return {"status": "success", "message": "Data ingested"}
