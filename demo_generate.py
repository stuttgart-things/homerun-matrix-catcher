from event_source.generate_source import RandomEventSource
from notification_sink import RGBSink
import asyncio
import argparse
import signal

# Example consumer function
async def example_consumer(event: dict):
    print(f"Received event: {event}")

async def main(rules, gen_gifs):
    file_source = RandomEventSource()
    rgb_sink = RGBSink(gen_gifs)

    # Register the example consumer
    file_source.register_consumer(rgb_sink.consume)
    file_source.register_consumer(example_consumer)

    # Start event sources
    await asyncio.gather(
        file_source.start(),
        rgb_sink.start(rules, gen_gifs)
    )
    
    print("Async functions have been interrupted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script that displays events in matrix")
    parser.add_argument("--profile", required=True, help="Yaml Rule file")
    parser.add_argument("--generategifs", action="store_true", help="Display generated gifs function")
    #parser.add_argument("--mock", required=False, action="store_true", help="Enable mock mode")
    args = parser.parse_args()

    profile_yaml = args.profile
    gen_gifs = args.generategifs
    #mock_mode = args.mock

    # Run the main function
    asyncio.run(main(profile_yaml, gen_gifs))#, mock_mode))