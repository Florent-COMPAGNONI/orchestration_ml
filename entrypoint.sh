#!/bin/sh

cd /app
# Start Memcached in the background
memcached -d


# Verify Memcached is running
if pgrep memcached > /dev/null
then
    echo "Memcached is running"
else
    echo "Failed to start Memcached"
    exit 1
fi

# Test Memcached connectivity
python3 -c "
import pymemcache.client.base as memcache
client = memcache.Client(('localhost', 11211))
try:
    client.set('key', 'value')
    value = client.get('key')
    if value == b'value':
        print('Memcached test succeeded')
    else:
        print('Memcached test failed')
except Exception as e:
    print('Memcached connection error:', e)
"

# Start the application
cd /app
uvicorn app:app --host 0.0.0.0 --port 8080