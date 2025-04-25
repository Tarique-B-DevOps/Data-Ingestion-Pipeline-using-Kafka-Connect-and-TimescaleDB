import json
import os
from kafka import KafkaConsumer

# Configuration
KAFKA_BROKER = 'localhost:29092'
TOPIC = os.getenv('KAFKA_TOPIC', 'sensor_data')

# Kafka Consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

if __name__ == "__main__":
    print(f"Consuming from topic: {TOPIC}")
    for message in consumer:
        print(f"Received: {message.value}")
