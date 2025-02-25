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

async def main(rules, gen_gifs, maxtime):
    # Create a Redis client
    #redis_client = redis.from_url("redis://localhost", decode_responses=True)

    stream_source = RedisStreamsSource()
    rgb_sink = RGBSink(gen_gifs)

    # Register the example consumer
    stream_source.register_consumer(rgb_sink.consume)
    stream_source.register_consumer(example_consumer)
    
    await stream_source.connection()
    

    
    await asyncio.gather(
        stream_source.start(),
        rgb_sink.start(rules, gen_gifs, maxtime)
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
    parser.add_argument("--generategifs", action="store_true", help="Display generated gifs function")
    parser.add_argument("--maxtime", type=int, default=5, required=False, help="Maximum time in seconds")
    #parser.add_argument("--events", required=True, help="File with json events")
    #parser.add_argument("--host", required=True, help="Redis host")
    #parser.add_argument("--port", required=True, help="Redis port")
    #parser.add_argument("--password", required=True, help="Redis password")
    args = parser.parse_args()

    profile_yaml = args.profile
    gen_gifs = args.generategifs
    maxtime = args.maxtime
    CHECK_WEIGHT = "empty"
    #events = args.events
    # Run the main function
    asyncio.run(main(profile_yaml, gen_gifs, maxtime))
