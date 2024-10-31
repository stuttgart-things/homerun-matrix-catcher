from event_source import StdinSource
from notification_sink import RGBSink_Image
import asyncio
import argparse
import signal
import time

async def main(image,time):
    rgb_sink = RGBSink_Image()

    # Start event sources
    await asyncio.gather(
        rgb_sink.start(image, time)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Settings for Text display.')
    parser.add_argument("-f", "--file", help="The image to show on the RGB LED panel", default="sthings.png")
    parser.add_argument("-t", "--time", help="Time in seconds for image to show on the RGB LED panel. '0' for infinity", default=5)
    args = parser.parse_args()
    # Run the main function
    asyncio.run(main(args.file,args.time))
