from event_source import StdinSource
from notification_sink import RGBSink
import asyncio
import argparse
import signal
import time

async def main(text):
    rgb_sink = RGBSink()

    # Start event sources
    await asyncio.gather(
        rgb_sink.start("Display_Text", text)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Settings for Text display.')
    parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!") 
    args = parser.parse_args()
    # Run the main function
    asyncio.run(main(args.text))
