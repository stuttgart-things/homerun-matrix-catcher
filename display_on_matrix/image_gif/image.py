import asyncio
import time
from PIL import Image
import requests

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
