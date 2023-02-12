#!/usr/bin/env bash

# Wait for postgres to be ready
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  echo "Waiting for postgres..."
  sleep 1
done

# Run the app
exec "$@"
