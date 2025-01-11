import argparse
import asyncio
import time
from PIL import Image
import requests
from unittest.mock import MagicMock

class YourClass:
    def __init__(self, mock):
        self.mock = mock
        self.matrix = self.initialize_matrix() if not mock else None
        self.queue = asyncio.Queue()
        self.stop_event = asyncio.Event()
        self.animation_task = None
        self.task = None
        self.flag_infinity = False
        self.pending_events = []
        self.event_args = None
        self.rules = None

    def initialize_matrix(self):
        try:
            # Attempt to initialize the matrix
            options = RGBMatrixOptions()
            options.rows = 64
            options.cols = 64
            options.chain_length = 1
            options.parallel = 1
            options.hardware_mapping = "adafruit-hat"
            return RGBMatrix(options=options)
        except RuntimeError as e:
            print(f"Failed to initialize matrix: {e}")
            return None

    async def display_task(self, event):
        print("Running event: " + str(event))

        if self.mock:
            print("Mock mode enabled, running mock function.")
            run_mock_test_image(event.get("args", {}))
            return

        if event["mode"].strip().lower() == "static":
            self.animation_task = asyncio.create_task(self.static_text(event.get("args", {}), ticker=False))

        elif event["mode"].strip().lower() == "text":
            self.animation_task = asyncio.create_task(self.flow_text(event.get("args", {}), ticker=False))

        elif event["mode"].strip().lower() == "ticker":
            self.animation_task = asyncio.create_task(self.flow_text(event.get("args", {}), ticker=True))

        elif event["mode"].strip().lower() == "image":
            self.animation_task = asyncio.create_task(self.display_image(event.get("args", {})))

        elif event["mode"].strip().lower() == "gif":
            self.animation_task = asyncio.create_task(self.display_gif(event.get("args", {})))

        if self.animation_task is not None:
            if self.flag_infinity:
                self.animation_task.cancel()
                self.flag_infinity = False
            else:
                result = await self.animation_task

        self.queue.task_done()
        self.event_args = None

    async def display_image(self, args):
        file_name = args.get("image")
        show_time = int(args.get("duration", 5))
        problem_files = []
        if show_time == 0:
            self.flag_infinity = True
        size = args.get("size", "full")
        if size != "full":
            size = size.split("x")
            image_width = int(size[0])
            image_height = int(size[1])
        else:
            image_width = self.matrix.width
            image_height = self.matrix.height
        offset_x, offset_y = 0, 0

        print(f"Animating '{file_name}'\n")
        ## Check if URL
        if "http" in file_name:
            image = Image.open(requests.get(file_name, stream=True).raw)
        else:
            image = Image.open("visual_aid/" + file_name)

        image.thumbnail((image_width, image_height), Image.ANTIALIAS)
        if image.width != self.matrix.width:
            offset_x = (self.matrix.width - image.width) / 2
        if image.height != self.matrix.height:
            offset_y = (self.matrix.height - image.height) / 2

        try:
            self.matrix.SetImage(image.convert('RGB'), offset_x, offset_y)
            time_start = time.time()
            while (time.time() < time_start + show_time) or show_time == 0:
                pass
            self.matrix.Clear()
            return

        except asyncio.CancelledError:
            print("heyoy")
            return

def run_mock_test_image(args):
    class MockMatrix:
        def __init__(self):
            self.width = 64
            self.height = 32

        def CreateFrameCanvas(self):
            return MagicMock()

        def SetImage(self, image, x, y):
            pass

        def Clear(self):
            pass

    class MockSelf:
        def __init__(self):
            self.matrix = MockMatrix()
            self.flag_infinity = False

    mock_self = MockSelf()

    asyncio.run(display_image(mock_self, args))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run display task with optional mock mode.")
    parser.add_argument("--mock", action="store_true", help="Enable mock mode")
    args = parser.parse_args()

    your_instance = YourClass(mock=args.mock)
    event = {"mode": "image", "args": {"image": "http://example.com/image.png", "duration": 5, "size": "full"}}
    asyncio.run(your_instance.display_task(event))