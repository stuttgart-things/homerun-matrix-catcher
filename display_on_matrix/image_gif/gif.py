import asyncio
import requests
from PIL import Image
import time
from helper_functions.arguments import get_speed

async def display_gif(self, args, mock): 
    if not mock:
        file_name = args.get("image")
        show_time = int(args.get("duration", 5))
        if show_time == 0:
            self.flag_infinity = True
        speed = get_speed(args.get("speed","5"))
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
    else:
        gif_name = args.get("image")
        duration = int(args.get("duration", 5))
        speed = get_speed(args.get("speed","5"))
        self.matrix.draw_gif(gif_name, duration, speed)