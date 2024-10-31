# write_to_redis.py
import redis
import json
from redis.commands.json.path import Path
import uuid
import os

redis_host = '192.168.1.205'
redis_port = 6379
redis_password = 'Atlan7is2024'

r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

try:
    print(f"Ping successful: {r.ping()}")
except Exception as e:
    print(f"Ping error: {e}")

stream_name = 'homerun:test'

# Beispiel-JSON-Daten
example_json_list = [
    {
        "Title": "image was build w/ kaniko on github workflows /images/***-alpine:2024-08-05",
        "Info": "/images/***-alpine:2024-08-05",
        "Severity": "info",
        "Author": "machineShop",
        "Timestamp": "08-05-2024 05:58:49",
        "System": "kaniko",
        "Tags": "[kaniko ghWorkflow]"
    },
    {
        "Title": "image was build w/ kaniko on github workflows /images/***-alpine:2024-08-05",
        "Info": "/images/***-alpine:2024-08-05",
        "Severity": "error",
        "Author": "machineShop",
        "Timestamp": "08-05-2024 05:58:49",
        "System": "gitlab",
        "Tags": "[kaniko ghWorkflow]"
    },
    {
        "Title": "image was build w/ kaniko on github workflows /images/***-alpine:2024-08-05",
        "Info": "/images/***-alpine:2024-08-05",
        "Severity": "info",
        "Author": "machineShop",
        "Timestamp": "08-05-2024 05:58:49",
        "System": "gitlab",
        "Tags": "[kaniko ghWorkflow]"
    }
]

# Funktion zum Erstellen eines JSON-Dokuments in RedisJSON
def create_json_in_redis(key, json_data):
    try:
        # JSON-Daten in RedisJSON speichern
        r.json().set(key, "$", json_data)
        print(f"JSON data stored successfully under key: {key}")
    except Exception as e:
        print(f"Error storing JSON data in Redis: {e}")

def create_message_in_stream(stream_name, message_data):
    try:
        message_id = r.xadd(stream_name, message_data)
        print(f"Message added to stream with ID: {message_id}")
        return message_id
    except Exception as e:
        print(f"Error adding message to stream: {e}")
        return None

def generate_random_id():
    return str(uuid.uuid4())

if __name__ == "__main__":
     for i, json_data in enumerate(example_json_list):

        print(json_data)
        randomID = generate_random_id()
        example_key = f"example:json:key:{randomID}"
        create_json_in_redis(randomID, json_data)

        create_message_in_stream(stream_name, {'messageID': randomID})
