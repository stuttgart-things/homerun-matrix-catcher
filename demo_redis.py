import redis
from event_source import RedisStreamsSource
import asyncio
from notification_sink import RGBSink
import argparse
import signal
import os

# Example consumer function
async def example_consumer(event: dict):
    print(f"Received event from  {event}")

async def main(rules):
    # Create a Redis client
    #redis_client = redis.from_url("redis://localhost", decode_responses=True)

    stream_source = RedisStreamsSource()
    rgb_sink = RGBSink()

    # Register the example consumer
    stream_source.register_consumer(rgb_sink.consume)
    stream_source.register_consumer(example_consumer)
    
    await stream_source.connection()
    

    
    await asyncio.gather(
        stream_source.start(),
        rgb_sink.start(rules)
    )

    # Wait indefinitely until a SIGTERM signal is received
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    def handle_sigterm():
        print("SIGTERM received, shutting down...")
        stream_source.stop()
        stop_event.set()

    loop.add_signal_handler(signal.SIGTERM, handle_sigterm)

    await stop_event.wait()

    # Close the Redis client connection
    await redis.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script that displays events in matrix")
    parser.add_argument("--profile", required=True, help="Yaml Rule file")
    #parser.add_argument("--events", required=True, help="File with json events")
    args = parser.parse_args()

    profile_yaml = args.profile
    #events = args.events
    # Run the main function
    asyncio.run(main(profile_yaml))
