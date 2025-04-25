#!/bin/bash

CONNECTOR_NAME="kafka-to-timescaledb"
TOPIC_NAME="${TOPIC_NAME}"
TABLE_NAME="${TOPIC_NAME}"
BATCH_SIZE=100

DB_HOST="timescaledb"
DB_PORT=5432
DB_NAME="timeseries"
DB_USER="postgres"
DB_PASSWORD="${DB_PASSWORD}"

CONNECT_URL="http://localhost:8085/connectors"

# ─── Create JDBC Sink Connector ───
curl -i -X POST \
  -H "Accept:application/json" \
  -H "Content-Type:application/json" \
  $CONNECT_URL -d '{
    "name": "'"$CONNECTOR_NAME"'",
    "config": {
      "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
      "task.max": "1",
      "topics": "'"$TOPIC_NAME"'",

      "key.converter": "org.apache.kafka.connect.json.JsonConverter",
      "key.converter.schemas.enable": "true",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "value.converter.schemas.enable": "true",
      "auto.create": "true",

      "transforms": "Flatten",
      "transforms.Flatten.type": "org.apache.kafka.connect.transforms.Flatten$Value",
      "transforms.Flatten.delimiter": "_",

      "connection.url": "jdbc:postgresql://'"$DB_HOST"':'"$DB_PORT"'/'"$DB_NAME"'",
      "connection.user": "'"$DB_USER"'",
      "connection.password": "'"$DB_PASSWORD"'",

      "insert.mode": "insert",
      "batch.size": "'"$BATCH_SIZE"'",

      "table.name.format": "'"$TABLE_NAME"'",
      "pk.mode": "none",
      "pk.fields": "id",

      "db.timezone": "Asia/Kolkata"
    }
  }'
