import json
import random
import time
import os
from kafka import KafkaProducer

# Configuration
KAFKA_BROKER = 'localhost:29092'
TOPIC = os.getenv('KAFKA_TOPIC', 'sensor_data')

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define schema
schema = {
    "type": "struct",
    "fields": [
        {"field": "id", "type": "int32"},
        {"field": "temperature", "type": "float"},
        {"field": "humidity", "type": "float"}
    ],
    "optional": False,
    "name": "iot_data"
}

def generate_sensor_data():
    return {
        "schema": schema,
        "payload": {
            "id": random.randint(1, 100),
            "temperature": round(random.uniform(20.0, 35.0), 2),
            "humidity": round(random.uniform(30.0, 70.0), 2)
        }
    }

if __name__ == "__main__":
    print(f"Producing to topic: {TOPIC}")
    while True:
        data = generate_sensor_data()
        producer.send(TOPIC, value=data)
        print(f"Produced: {data}")
        time.sleep(1)
