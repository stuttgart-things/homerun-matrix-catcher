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
from helper_functions.eventtime_comparison.compare_time import evaluate_event_timing

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
        self.rules = self.get_rules(rules_file)
        self.task = asyncio.create_task(self.run())

    async def stop(self):
        if self.task:
            self.task.Cancel()
            self.task = None

    def get_rules(self, rules_yaml):
        with open(rules_yaml, 'r') as file:
            configuration = yaml.safe_load(file)
        configuration = configuration["matrixConfig"]

        rules = {}
        for key, value in configuration.items():
            rules[key] = {
                'kind': value.get('kind'),
                'severity': value.get('severity'),
                'systems': value.get('systems')
            }
            # Conditionally add 'text' if it is not None
            if value.get('text') is not None:
                rules[key]['text'] = value.get('text')
                rules[key]['font'] = value.get('font')
            # Conditionally add 'image' if it is not None
            if value.get('image') is not None:
                rules[key]['image'] = value.get('image')
            # Conditionally add 'duration' if it is not None
            if value.get('duration') is not None:
                rules[key]['duration'] = value.get('duration')

        print("Rules: ", rules)
        return rules

    def get_arguments(self, rules, event):
        event_args = []
        event_args.clear()
        print("/////////////////////////////////////")
        print(event)
        print("/////////////////////////////////////")
        for rule_name, rule in rules.items():
            if event_args:
                break
            kind = rule.get('kind')
            severitys = rule.get('severity')
            systems = rule.get('systems')
            event_system = event.get('system')
            event_severity = event.get('severity')
            event_timestamp = event.get('timestamp')

            print(f"Checking rule: {rule_name}")
            print(f"Event system: {event_system}, Event severity: {event_severity}")
            print(f"Rule systems: {systems}, Rule severity: {severitys}")

            args = {}  # Create a new args dictionary for each rule

            # Check if the event matches the rule's systems and severity
            if event_system  in systems and event_severity in severitys:
                # If the rule has a text key, process it
                if kind in ["static", "text", "ticker"]:
                    print_text = rule.get('text')
                    print_text = Template(print_text).render(**event)
                    args["text"] = print_text
                    args['font'] = rule.get('font')
                # Add other arguments from the rule
                elif kind in ["gif", "image"]:
                    args['image'] = rule.get('image')

                event_args.append({"mode": kind, "severity": severitys, "systems": systems, "timestamp": event_timestamp, "args": args})
        print(f"Generated event arguments: {event_args}")
        return event_args

    async def build_event_list(self):
        print("in build")
        #severity_dict, systems_dict, argument_dict = self.get_rules(self.rules)
        while True:
            event_json = await self.queue.get()
            print(f"Processing event: {event_json}")##########
            event_args = self.get_arguments(self.rules, event_json["event"])
            if event_args:
                self.pending_events += event_args
            print("\npending events")
            print(self.pending_events)
            print("\n\n")

    async def run_event_list(self):
        while True:
            print(f"evaluating pending events, {len(self.pending_events)} left")
            if self.pending_events:
                print("Popping event")
                event_args = self.pending_events.pop(0)
                print(f"Popped event: {event_args}")
                time_difference, log, event_expired = evaluate_event_timing(event_args, 15)
                if not event_expired:
                    print(f"Running event: {event_args}")
                    await self.display_task(event_args)
                else:
                    print("Events expired not showing")

            else:
                print("No events found, sleeping")
                await asyncio.sleep(1)
                

    async def display_task(self, event):
        print("Running event: " + str(event))

        if event["mode"].strip().lower()=="static":
            self.animation_task = asyncio.create_task(self.static_text(event.get("args",{}),ticker=False))

        elif event["mode"].strip().lower()=="text":
            self.animation_task = asyncio.create_task(self.flow_text(event.get("args",{}),ticker=False))

        elif event["mode"].strip().lower()=="ticker":
            self.animation_task = asyncio.create_task(self.flow_text(event.get("args",{}),ticker=True))

        elif event["mode"].strip().lower()=="image":
            self.animation_task = asyncio.create_task(self.display_image(event.get("args",{})))

        elif event["mode"].strip().lower()=="gif":
            self.animation_task = asyncio.create_task(self.display_gif(event.get("args",{})))


        if self.animation_task != None:
            if self.flag_infinity:
                self.animation_task.cancel()
                self.flag_infinity = False
            else:
                result = await self.animation_task
        #if selfs.animation_task != None and self.flag_infinity:

        self.queue.task_done()
            
        self.event_args=None

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

    def get_speed(self, speed):
        sleep_dict = {"5": 0.01, "4": 0.03, "3": 0.05, "2":0.1, "1":0.2}
        return sleep_dict[str(speed)]

    def get_color(self, color):
        color = color.replace("(","").replace(")","").replace(" ","")
        color = color.split(",")
        return color 

    async def flow_text(self, args, ticker = True): #, loops=5, font_sytle="./spleen-32x64.bdf"):
        text = args.get("text")
        font_style = args.get("font", "quattrocento48.bdf")
        color = self.get_color(args.get("color","255,192,203"))
        speed = self.get_speed(args.get("speed","5"))
        loops =  int(args.get("loops", 1))
        show_time = int(args.get("duration", 5))

        print(f"Animating '{text}'\n")
        loop = asyncio.get_running_loop()

        offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        font = graphics.Font()
        font.LoadFont("fonts/" + font_style)

        if font.baseline <= offscreen_canvas.height:
            #Center the text vertically
            pos_y = int(font.baseline - (offscreen_canvas.height/2 - font.baseline/2))
        else:
            pos_y = int(font.baseline + (offscreen_canvas.height/2 - font.baseline/2))

        textcolor = graphics.Color(int(color[0]),int(color[1]),int(color[2]))
        
        pos_x = offscreen_canvas.width
        
        if ticker:
            await self.ticker_text(offscreen_canvas, font, pos_x, pos_y, textcolor, text, loop, loops, speed)
        else:
            await self.timed_text(offscreen_canvas, font, pos_x, pos_y, textcolor, text, loop, show_time, speed)

        return
    
    async def ticker_text(self, offscreen_canvas, font, pos_x, pos_y, textcolor, text, loop, loops, speed):
        try:
            while loops > 0:
                offscreen_canvas.Clear()
                length = graphics.DrawText(offscreen_canvas, font, pos_x, pos_y, textcolor, text)
                pos_x -= 1

                if (pos_x + length < 0):
                    loops -= 1
                    pos_x = offscreen_canvas.width

                offscreen_canvas = await loop.run_in_executor(None, self.matrix.SwapOnVSync, offscreen_canvas)
                # adapt to modify speed
                await asyncio.sleep(speed)

        except asyncio.CancelledError:
            print("cancelado")
            return "error"

    async def static_text(self, args, ticker = True): #, loops=5, font_sytle="./spleen-32x64.bdf"):
        print("SHOWING STATIC TEXT")
        text = args.get("text")
        font_style = args.get("font", "quattrocento48.bdf")
        color = self.get_color(args.get("color","255,192,203"))
        speed = self.get_speed(args.get("speed","5"))
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
        speed = self.get_speed(args.get("speed","2"))
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
