#!/bin/sh

# Start Memcached in the background
memcached -d

# Start the application
uvicorn app:app --host 0.0.0.0 --port 8080