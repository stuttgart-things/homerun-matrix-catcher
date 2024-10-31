from event_source import StdinSource
from notification_sink import RGBStdinSink
import asyncio

import signal


# Example consumer function
async def example_consumer(event: dict):
    print(f"Received event: {event}")


async def main():
    stdin_source = StdinSource()

    rgb_sink = RGBStdinSink()

    # Register the example consumer
    stdin_source.register_consumer(rgb_sink.consume)
    stdin_source.register_consumer(example_consumer)

    # Start event sources
    await asyncio.gather(
        stdin_source.start(),
        rgb_sink.start()
    )
    
    # Wait indefinitely until a SIGTERM signal is received
    #stop_event = asyncio.Event()
    #loop = asyncio.get_running_loop()
    
    #def handle_sigterm():
    #    print("SIGTERM received, shutting down...")
    #    stop_event.set()

    #loop.add_signal_handler(signal.SIGTERM, handle_sigterm)

    #await stop_event.wait()


# Run the main function
asyncio.run(main())
