# Data Ingestion Pipeline using Kafka Connect & TimescaleDB

This project sets up a data ingestion pipeline using Kafka, Kafka Connect, and TimescaleDB. It allows you to stream data from Kafka topics into TimescaleDB and process it in real-time.

## Setting Up and Testing Environment

This section walks through setting up the Docker-based stack and verifying ingestion using Kafka and TimescaleDB.

### 1 - Spin up Docker Compose Stack

Start the entire stack by running:

Export the required environment variables:

```bash
export DB_PASSWORD=postgres TOPIC_NAME=sensor_data
```

```bash
docker compose up -d
```

This will spin up the following services:
- **Zookeeper**: For managing Kafka brokers.
- **Kafka**: The message broker.
- **Schema Registry**: Manages Avro schema versions.
- **Kafka Connect**: The Kafka connector framework.
- **TimescaleDB**: A PostgreSQL extension for time-series data.

### 2 - Ensure All Containers Are Running

You can verify that all the containers are up and running by executing:

```bash
docker compose ps
```

This will list all the services in your stack and their current status.

### 3 - Create Connector by Running the Script

In the project directory, you can create the Kafka Connect sink connector to ingest data into TimescaleDB by running the script:

```bash
./create-sink-timescaledb-connector.sh
```

This script will create the connector that takes data from Kafka (through a topic) and inserts it into TimescaleDB.

### 4 - Start Consumer to Check If You Are Receiving Messages

In one terminal window, run the Kafka console consumer to check if the producer messages are being consumed:

```bash
TOPIC_NAME=sensor_data; docker exec -i kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic $TOPIC_NAME --from-beginning
```


### 5 - Start Kafka Console Producer Using Docker Exec Command

In another terminal window, run the Kafka console producer by executing:

```bash
TOPIC_NAME=sensor_data; docker exec -i kafka kafka-console-producer --broker-list localhost:9092 --topic $TOPIC_NAME <<< '{"schema":{"type":"struct","fields":[{"field":"id","type":"int32"},{"field":"temperature","type":"float"},{"field":"humidity","type":"float"}],"optional":false,"name":"iot_data"},"payload":{"id":1,"temperature":25.3,"humidity":60.2}}'
```

In the consumer's terminal window, verify that the message has been received


### 6 - Check Kafka Connector Logs

You can view the logs of your Kafka Connect connector to ensure it is processing and pushing data to TimescaleDB by running:

```bash
docker compose logs -f
```

Or, to view just the connector logs:

```bash
docker compose logs -f kafkaconnect
```

If there are no errors in the logs, it means that data is being successfully saved in the TimescaleDB.

### 7 - Lastly, Use PSQL CLI or Tools Like pgAdmin to Verify and View the Data

To verify that the data is saved in TimescaleDB, you can either use the `psql` command line tool or a GUI tool like pgAdmin. To use `psql`, run the following command:

```bash
psql -h localhost -U postgres -d timeseries
```

Then, list the tables and query the data in the appropriate table:

```bash
\dt
```
```bash
SELECT * FROM sensor_data LIMIT 10;
```

This will allow you to verify the data inserted into your TimescaleDB.

## Stream and Consume Ingested Data in Real-Time

To test the ingestion pipeline using Python scripts in real-time, follow these steps:

1. **Create and activate a virtual environment**

    ```bash
    python3 -m venv venv
    ```
    ```bash  
    source venv/bin/activate
    ```

2. **Install required dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the producer**

    Start the data producer which sends random sensor data to the Kafka topic:

    ```bash
    python3 producer.py
    ```

4. **Run the Kafka topic consumer**

    In a new terminal tab, run the consumer to verify messages are received directly from the Kafka topic:

    ```bash
    python3 consumer.py
    ```

5. **Run the TimescaleDB consumer**

    In another terminal tab, run the DB consumer to verify ingested data from the TimescaleDB:

    ```bash
    python3 consumer-db.py
    ```
This setup helps validate both Kafka ingestion and TimescaleDB storage in real-time.
