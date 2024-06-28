FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install Memcached
RUN apt-get update && \
    apt-get install -y memcached && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Expose the default Memcached port
EXPOSE 11211

COPY . .

RUN chmod +x /entrypoint.sh