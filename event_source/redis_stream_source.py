from typing import Callable, List
import asyncio
import os
import json
import uuid
from redis.commands.json.path import Path
from event_source.event_source import EventSource
import redis.asyncio as redis

class RedisStreamsSource(EventSource):
    def __init__(self):
        self.task = None
        self.connect = None 
        self.r = None
        self.consumers: List[Callable[[str, dict], None]] = []

        
        self.redis_host = '192.168.1.121'
        self.redis_port = 6379
        self.redis_password = 'Atlan7is2025'

        self.pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, password=self.redis_password, decode_responses=True)
        self.r = redis.Redis(connection_pool=self.pool)
        
        self.stream_name = 'scaletest'
        self.group_name = 'homerun'
        self.consumer_name = 'python-test-consumer'


    async def check_connection(self):
        print("Checking redis connection...")
        try:
            ping_result = await self.r.ping()
            print(f"Ping successful: {ping_result}")
        except Exception as e:
            print(f"Ping error: {e}")

    async def create_group_if_not_exists(self):
        try: 
            groups = await self.r.xinfo_groups(self.stream_name)
            if not any([group["name"] == self.group_name for group in groups]):
                await self.r.xgroup_create(self.stream_name, self.group_name, id='0', mkstream=True)
        except Exception as e:
            print (f"Consumer Group Error: {e}")
                

    async def _read_stream(self):
        """Continuously read from the Redis stream and notify consumers."""      
        print("in _read")

        await self.check_connection()
        print("Happy Reading!")
        while True:
            try:
                # Read new events from the stream
                events = await self.r.xreadgroup(self.group_name, self.consumer_name, {self.stream_name: '>'}, count=10, block=0)
                for stream, messages in events:
                    for message_id, message in messages:

                        # GET JSON ID
                        jsonID = message['messageID']

                        # READ JSON ID
                        event = await self.read_json(jsonID)
                        await self.write_event({"event": event})

                        # ACKNOWLEDGE MESSAGE
                        await self.r.xack(self.stream_name, self.group_name, message_id)


            except Exception as e:
                print(f"Error reading from stream: {e}")
                return


    async def read_json(self, jsonID):
       # Read JSON data using JSON.GET command
        try:
            event = await self.r.json().get(jsonID, "$")
            return event[0]

        except Exception as e:
            print(f"Error retrieving JSON data: {e}")



    async def write_event(self, event):
        print(event)
        """Notify consumers."""
        await self._notify_consumers(event)



    async def run(self):
        try:
            print("running redis stream\n")
            await self._read_stream()
            print("done with stream")
            return

        except Exception as e:
            print(f"Error in stream: {e}")



    async def connection(self):
        self.connect = asyncio.create_task(self.redis_client())

    async def redis_client(self): 
        await self.check_connection()
        await self.create_group_if_not_exists()



    async def start(self):
        print ("in start") 
        """Start the consumer task."""
        self.task = asyncio.create_task(self.run())

    async def stop(self):
        """Stop the consumer task."""
        if self.task:
            self.task.cancel()
            self.task = None

        if self.connect:
            self.connect.cancel()
            self.cancel = None

