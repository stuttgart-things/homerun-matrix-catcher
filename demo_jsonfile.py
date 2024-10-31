from event_source import JsonFileSource
from notification_sink import RGBSink
import asyncio
import argparse
import signal


# Example consumer function
async def example_consumer(event: dict):
    print(f"Received event: {event}")


async def main(rules,events):
    file_source = JsonFileSource()
    rgb_sink = RGBSink()

    # Register the example consumer
    file_source.register_consumer(rgb_sink.consume)
    file_source.register_consumer(example_consumer)

    # Start event sources
    await asyncio.gather(
        file_source.start(events),
        rgb_sink.start(rules)
    )
    
    print("Async functions have been interrupted.")
    # Wait indefinitely until a SIGTERM signal is received
    #stop_event = asyncio.Event()
    #loop = asyncio.get_running_loop()
    
    #def handle_sigterm():
    #    print("SIGTERM received, shutting down...")
    #    stop_event.set()

    #loop.add_signal_handler(signal.SIGTERM, handle_sigterm)

    #await stop_event.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script that displays events in matrix")
    parser.add_argument("--profile", required=True, help="Yaml Rule file")
    parser.add_argument("--events", required=True, help="File with json events")
    args = parser.parse_args()

    profile_yaml = args.profile
    events = args.events
    # Run the main function
    asyncio.run(main(profile_yaml,events))
