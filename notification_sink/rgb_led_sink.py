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
from helper_functions.arguments import get_arguments, get_speed, get_color
from helper_functions.event_list import build_event_list, run_event_list
from helper_functions.rules import get_rules

class RGBSink():
    def __init__(self):
        options = RGBMatrixOptions()

        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "adafruit-hat"

        self.matrix = RGBMatrix(options = options)
        self.queue = asyncio.Queue()

        self.stop_event = asyncio.Event()
        self.animation_task = None
        self.task = None

        self.flag_infinity = False
        self.pending_events = []
        self.event_args = None
        self.rules = None

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
    
#    async def ticker_text(self, offscreen_canvas, font, pos_x, pos_y, textcolor, text, loop, loops, speed):
#        try:
#            while loops > 0:
#                offscreen_canvas.Clear()
#                length = graphics.DrawText(offscreen_canvas, font, pos_x, pos_y, textcolor, text)
#                pos_x -= 1
#
#                if (pos_x + length < 0):
#                    loops -= 1
#                    pos_x = offscreen_canvas.width
#
#                offscreen_canvas = await loop.run_in_executor(None, self.matrix.SwapOnVSync, offscreen_canvas)
#                # adapt to modify speed
#                await asyncio.sleep(speed)
#
#        except asyncio.CancelledError:
#            print("cancelado")
#            return "error"

    async def static_text(self, args, ticker = True): #, loops=5, font_sytle="./spleen-32x64.bdf"):
        print("SHOWING STATIC TEXT")
        text = args.get("text")
        font_style = args.get("font", "quattrocento48.bdf")
        color = get_color(args.get("color","255,192,203"))
        speed = get_speed(args.get("speed","5"))
        show_time = int(args.get("duration", 5))

        print(f"Animating '{text}'\n")
        loop = asyncio.get_running_loop()

        offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        font = graphics.Font()
        font.LoadFont("fonts/" + font_style)
        print(f"Baseline: {font.baseline}, Canvas-height: {offscreen_canvas.height}, Canvas-width : {offscreen_canvas.width}")
        if font.baseline >= offscreen_canvas.height:
            # centers the text with offset of 4
            pos_y = int((offscreen_canvas.height - font.baseline) / 2 + font.baseline + 4)
            # pos_y = int(font.baseline - (offscreen_canvas.height/2 - font.baseline/2))
        else:
            # centers the text with offset of 4
            pos_y = int((offscreen_canvas.height - font.baseline) / 2 + font.baseline - 4)
            # pos_y = int(font.baseline + (offscreen_canvas.height/2 - font.baseline/2))
        
        textcolor = graphics.Color(int(color[0]),int(color[1]),int(color[2]))

        # Manually calculate the width of the text
        # text_width = sum(font.CharacterWidth(ord(char)) for char in text)
        text_width = graphics.DrawText(offscreen_canvas, font, 0, pos_y, textcolor, text)
        # Calculate the starting x position to center the text
        pos_x = ((offscreen_canvas.width - (text_width - 2)) / 2)

        offscreen_canvas.Clear()
        graphics.DrawText(offscreen_canvas, font, pos_x, pos_y, textcolor, text)
        offscreen_canvas = await loop.run_in_executor(None, self.matrix.SwapOnVSync, offscreen_canvas)

        await asyncio.sleep(10)
        return

    async def timed_text(self, offscreen_canvas, font, pos_x, pos_y, textcolor, text, loop, show_time, speed):
        try:
            time_start = time.time()
            while True :  #To interrupt after time is done or to finish run?
                done_flag = False
                offscreen_canvas.Clear()
                length = graphics.DrawText(offscreen_canvas, font, pos_x, pos_y, textcolor, text)
                pos_x -= 1

                if (pos_x + length < 0):
                    pos_x = offscreen_canvas.width
                    if time.time() > time_start + show_time: break

                offscreen_canvas = await loop.run_in_executor(None, self.matrix.SwapOnVSync, offscreen_canvas)
                
                # adapt to modify speed
                await asyncio.sleep(speed)
        except asyncio.CancelledError:
            return "error"
        return

    async def display_image(self, args):
        file_name = args.get("image")
        show_time = int(args.get("duration", 5))
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
        offset_x, offset_y= 0, 0

        print(f"Animating '{file_name}'\n")
        ## Check if URL
        if "http" in file_name:
            image = Image.open(requests.get(file_name, stream=True).raw) 
        else:
            image = Image.open("visual_aid/" + file_name)

        image.thumbnail((image_width, image_height), Image.ANTIALIAS)
        if image.width != self.matrix.width: offset_x = (self.matrix.width - image.width)/2
        if image.height != self.matrix.height: offset_y = (self.matrix.height - image.height)/2

        try:
            self.matrix.SetImage(image.convert('RGB'), offset_x, offset_y)
            #if show_time != 0:
            
            time_start = time.time()
            while (time.time() < time_start + show_time) or show_time == 0:
                pass
            self.matrix.Clear()
            return
            
        
        except asyncio.CancelledError:
            print("heyoy")
            return
                
    
    async def display_gif(self, args): 
        file_name = args.get("image")
        show_time = int(args.get("duration", 5))
        if show_time == 0:
            self.flag_infinity = True
        speed = get_speed(args.get("speed","2"))
        size = args.get("size", "full")
        if size != "full":
            size = size.split("x")
            image_width = int(size[0])
            image_height = int(size[1])
        else:
            image_width = self.matrix.width
            image_height = self.matrix.height
        offset_x, offset_y= 0, 0

        if "http" in file_name:
            save_as = file_name.split("/")[-1]
            with open(f'/tmp/{save_as}', 'wb') as f:
                f.write(requests.get(file_name).content)
            gif = Image.open("/tmp/" + save_as)#, stream=True).raw)
        else:
            gif = Image.open("visual_aid/" + file_name)

        try:
            num_frames = gif.n_frames
        except Exception:
            exit("provided image is not a gif")
            return
        
        #Preprocess the gifs frames into canvases to improve playback performance
        canvases = []
        offset_x, offset_y = 0, 0
        loop = asyncio.get_running_loop()
        
        for frame_index in range(0, num_frames):
            gif.seek(frame_index)
            frame = gif.copy()
            frame.thumbnail((image_width, image_height), Image.ANTIALIAS)
            
            if frame.width != self.matrix.width: offset_x = (self.matrix.width - frame.width)/2
            if frame.height != self.matrix.height: offset_y = (self.matrix.height - frame.height)/2

            offscreen_canvas = self.matrix.CreateFrameCanvas()
            offscreen_canvas.SetImage(frame.convert("RGB"), offset_x, offset_y)
            canvases.append(offscreen_canvas)
        # Close the gif file to save memory now that we have copied out all of the frames
        gif.close()
        print("Completed Preprocessing, displaying gif\n")
        try:
            # Infinitely loop through the gif
            cur_frame = num_frames
            time_start = time.time()
            while (time.time() < time_start + show_time) or show_time == 0:
                if cur_frame >= num_frames - 1:
                    cur_frame = 0
                else:
                    cur_frame += 1
                
                await loop.run_in_executor(None, self.matrix.SwapOnVSync, canvases[cur_frame])
                await asyncio.sleep(speed)
                
            self.matrix.Clear()
        
        except asyncio.CancelledError:
            return
