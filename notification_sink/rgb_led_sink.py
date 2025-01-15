import datetime
from typing import Dict
from rgbmatrix import RGBMatrix, RGBMatrixOptions,graphics
import time
from concurrent.futures import ThreadPoolExecutor
from jinja2 import Template
import pprint
import asyncio
import json, yaml
from PIL import Image
import requests
import numpy as np
from io import BytesIO
from display_on_matrix.display_logic import display_task
from display_on_matrix.text.flow import flow_text
from display_on_matrix.text.timed import timed_text
from display_on_matrix.text.ticker import ticker_text
from display_on_matrix.text.static import static_text
from display_on_matrix.image_gif.image import display_image
from display_on_matrix.image_gif.gif import display_gif
from helper_functions.arguments import get_speed, get_color
from helper_functions.event_list import build_event_list, run_event_list
from helper_functions.rules import get_rules

class RGBSink():
    def __init__(self, mock):
        #options = RGBMatrixOptions()

        #options.rows = 64
        #options.cols = 64
        #options.chain_length = 1
        #options.parallel = 1
        #options.hardware_mapping = "adafruit-hat"

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

    async def start(self, rules_file):
        self.rules = get_rules(rules_file)
        self.task = asyncio.create_task(self.run())

    async def stop(self):
        if self.task:
            self.task.Cancel()
            self.task = None

    async def build_event_list(self):
        await build_event_list(self.queue, self.rules, self.pending_events)

    async def run_event_list(self):
        await run_event_list(self.pending_events, self.display_task)

    async def display_task(self, event):
        await display_task(self, event)

    async def run(self):
        try:
            ###
            print("running rgb sink\n")
            #for e in event_list:
            
            await asyncio.gather(
                self.build_event_list(),
                self.run_event_list()
            )
            #await self.build_event_list()
            #await self.run_event_list()
            print("Im outside")
            return
        except asyncio.CancelledError:
            print("Cancelled Error within RGBSink")
            return

    async def consume(self, data : dict):
        print(f"Consuming event: {data}")#########
        await self.queue.put(data)

    # Unused/untested for now 05.12.24
    async def flow_text(self, args, ticker=True):
        await flow_text(self, args, ticker)

    # Unused/untested for now 06.12.24
    async def ticker_text(self, offscreen_canvas, font, pos_x, pos_y, textcolor, text, loop, loops, speed):
        await ticker_text(self, offscreen_canvas, font, pos_x, pos_y, textcolor, text, loop, loops, speed)

    # Unused/untested for now 06.12.24
    async def timed_text(self, offscreen_canvas, font, pos_x, pos_y, textcolor, text, loop, show_time, speed):
        await timed_text(self, offscreen_canvas, font, pos_x, pos_y, textcolor, text, loop, show_time, speed)

    async def static_text(self, args, ticker=True):
        await static_text(self, args, ticker)

    async def display_image(self, args):
        await display_image(self, args)

    async def display_gif(self, args):
        await display_gif(self, args)
