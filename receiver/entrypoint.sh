#!/bin/sh

echo "Waiting for kafka..."

while ! kafkacat -b kafka:9092 -L; do
    sleep 0.1
done

echo "Kafka started"

exec "$@"