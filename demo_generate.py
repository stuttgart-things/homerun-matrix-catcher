from event_source.generate_source import RandomEventSource
from notification_sink import RGBSink
import asyncio
import argparse
import signal

# Example consumer function
async def example_consumer(event: dict):
    print(f"Received event: {event}")

async def main(rules):
    file_source = RandomEventSource()
    rgb_sink = RGBSink()

    # Register the example consumer
    file_source.register_consumer(rgb_sink.consume)
    file_source.register_consumer(example_consumer)

    # Start event sources
    await asyncio.gather(
        file_source.start(),
        rgb_sink.start(rules)
    )
    
    print("Async functions have been interrupted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script that displays events in matrix")
    parser.add_argument("--profile", required=True, help="Yaml Rule file")
    args = parser.parse_args()

    profile_yaml = args.profile

    # Run the main function
    asyncio.run(main(profile_yaml))