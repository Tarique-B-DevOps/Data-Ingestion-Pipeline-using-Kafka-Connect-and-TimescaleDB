#!/bin/bash

CONNECT_URL="http://localhost:8085/connectors"

CONNECTORS=$(curl -s -X GET -H "Accept:application/json" $CONNECT_URL)

for CONNECTOR in $(echo $CONNECTORS | jq -r '.[]'); do
  echo "Deleting connector: $CONNECTOR"
  curl -s -X DELETE $CONNECT_URL/$CONNECTOR
  echo "Connector $CONNECTOR deleted."
done

echo "All connectors have been deleted."
