import os
import json
import uuid
import logging
from datetime import datetime
from threading import Thread
from typing import Any, Dict

from fastapi import FastAPI, Request, HTTPException, status
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

from schemas.movie import Movie
from schemas.user import User
from schemas.payment import Payment

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Kafka configuration
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:9092")
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logger.info("Kafka producer initialized")
except Exception as e:
    logger.warning(f"Kafka producer initialization failed: {e}")
    producer = None

# Consumer runs in background thread
consumer_thread: Thread = None
consumer_running = False

def start_consumer():
    global consumer_running
    consumer_running = True
    topics = ["movie-events", "user-events", "payment-events"]
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=KAFKA_BROKERS,
        group_id="events-service-consumer",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )
    logger.info("Kafka consumer started for topics: %s", ", ".join(topics))
    try:
        for message in consumer:
            if not consumer_running:
                break
            logger.info(
                "Consumed message from topic %s partition %d offset %d: %s",
                message.topic,
                message.partition,
                message.offset,
                json.dumps(message.value),
            )
    finally:
        consumer.close()
        logger.info("Kafka consumer stopped")

def produce_event(topic: str, payload: Dict[str, Any]):
    if producer is None:
        logger.warning("Kafka producer not available; skipping event production for %s", topic)
        raise HTTPException(status_code=503, detail="Kafka broker unavailable")
    
    if hasattr(payload, 'dict'):
        payload_dict = payload.dict()
    else:
        payload_dict = payload
    
    event = {
        "id": str(uuid.uuid4()),
        "type": topic.replace('-events', ''),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "payload": payload_dict,  # Используем словарь вместо объекта
    }
    
    future = producer.send(topic, event)
    try:
        record_metadata = future.get(timeout=10)
        logger.info(
            "Produced event to %s partition %d offset %d",
            record_metadata.topic,
            record_metadata.partition,
            record_metadata.offset,
        )
        return {
            "status": "success"
        }
    except KafkaError as e:
        logger.error("Failed to send message to Kafka: %s", e)
        raise HTTPException(status_code=500, detail="Kafka error")

@app.get("/api/events/health")
async def health():
    return {"status": True}

@app.post("/api/events/movie", status_code=status.HTTP_201_CREATED)
async def create_movie_event(movie: Movie):
    return produce_event("movie-events", movie)

@app.post("/api/events/user", status_code=status.HTTP_201_CREATED)
async def create_user_event(user: User):
    return produce_event("user-events", user)

@app.post("/api/events/payment", status_code=status.HTTP_201_CREATED)
async def create_payment_event(payment: Payment):
    return produce_event("payment-events", payment)

@app.on_event("startup")
async def startup_event():
    global consumer_thread
    # Start background consumer thread
    consumer_thread = Thread(target=start_consumer, daemon=True)
    consumer_thread.start()
    logger.info("Events service started")

@app.on_event("shutdown")
async def shutdown_event():
    global consumer_running
    consumer_running = False
    # Give consumer a moment to exit
    if consumer_thread is not None:
        consumer_thread.join(timeout=5)
    producer.flush()
    producer.close()
    logger.info("Events service stopped")
