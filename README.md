# TealOrca Assignment

This project simulates time-series data from IoT devices, streams it to a frontend via WebSocket, and performs batch inserts into TimescaleDB using Kafka. The stack includes FastAPI, Kafka, TimescaleDB, Docker, and WebSockets.

---

## Features

- FastAPI backend with Kafka integration
- TimescaleDB for efficient time-series storage
- Real-time data streaming via WebSocket
- IoT simulator for temperature, humidity, and SOx (hard coded only in simulator but the backend is completely flexible)
- Batch insert into DB every 5 seconds

---

## Prerequisites

- Python 3.10.x
- Docker & Docker Compose installed

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kshatriya-25/tealorcaAssignment.git
cd tealorcaAssignment
```

### 2. Create & Activate Virtual Environment

On macOS/Linux:

```bash
python3.10 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python3.10 -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Infrastructure Setup

Start the infrastructure using Docker Compose:

```bash
docker-compose up
```

This will start Kafka, TimescaleDB, and other necessary services like Zookeeper, etc.

---

## Running the Application

### 1. Run Migrations

```bash
alembic upgrade head
```

### 2. Create Parameters

Before running the simulator, you need to create parameters for the data types you plan to simulate. The required ones are:

- `temperature`
- `humidity`
- `sox`

You can create them via the following `curl` command (or paste them in Postman):

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/parameter/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'name=sox&unit=string&description=string'
```

Repeat this for `temperature` and `humidity` with appropriate values.

Alternatively, you can use the Swagger UI at the following URL:

[http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)

### 3. Run the Simulator

```bash
python3.10 simulator.py
```

### 4. View WebSocket Data in the UI

You can view the WebSocket data in the UI at the following URL:

[http://localhost:8000/web/index.html](http://localhost:8000/web/index.html)

### 5. Batch Insert Data into TimescaleDB

Run the service file using the following command:

```bash
PYTHONPATH=. python3.10 app/api/kafka_consumer/batchInset.py
```