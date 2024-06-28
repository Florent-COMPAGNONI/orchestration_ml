#!/bin/sh

cd /app

# Start Memcached in the background
memcached -d -u nobody

# Run Fast API
uvicorn app:app --host 0.0.0.0 --port 8080