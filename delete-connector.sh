#!/bin/bash

CONNECT_URL="http://localhost:8085/connectors"

if [ -z "$1" ]; then
  echo "Please provide a connector name."
  echo "Usage: $0 <connector_name>"
  exit 1
fi

CONNECTOR_NAME=$1

echo "Deleting connector: $CONNECTOR_NAME"
curl -s -X DELETE $CONNECT_URL/$CONNECTOR_NAME

echo "Connector $CONNECTOR_NAME deleted."
