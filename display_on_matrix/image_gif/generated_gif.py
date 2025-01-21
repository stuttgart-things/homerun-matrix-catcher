import asyncio
import requests
from PIL import Image
import time
from helper_functions.arguments import get_speed
from display_on_matrix.generate_gifs.create_gifs import create_frame, generate_gif

async def display_generated_gif(self, args, event): 
    file_name = args.get("image")
    show_time = int(args.get("duration", 5))
    display_severity = event.get("severity")
    display_system = event.get("systems")

    if show_time == 0:
        self.flag_infinity = True

    speed = get_speed(args.get("speed", "2"))
    size = args.get("size", "full")

    if size != "full":
        size = size.split("x")
        image_width = int(size[0])
        image_height = int(size[1])
    else:
        image_width = self.matrix.width
        image_height = self.matrix.height

    offset_x, offset_y = 0, 0

    gif_path = generate_gif(display_severity, display_system)

    gif = Image.open(gif_path)

    try:
        num_frames = gif.n_frames
    except Exception:
        exit("provided image is not a gif")
        return

    # Preprocess the gif frames into canvases to improve playback performance
    canvases = []
    frame_durations = []
    loop = asyncio.get_running_loop()

    for frame_index in range(num_frames):
        gif.seek(frame_index)
        frame = gif.copy()
        frame.thumbnail((image_width, image_height), Image.ANTIALIAS)

        if frame.width != self.matrix.width:
            offset_x = (self.matrix.width - frame.width) // 2
        if frame.height != self.matrix.height:
            offset_y = (self.matrix.height - frame.height) // 2

        offscreen_canvas = self.matrix.CreateFrameCanvas()
        offscreen_canvas.Clear()  # Clear the canvas before drawing the new frame
        offscreen_canvas.SetImage(frame.convert("RGB"), offset_x, offset_y)
        canvases.append(offscreen_canvas)

        # Get the duration of the current frame
        frame_durations.append(gif.info.get('duration', 100) / 1000)  # Convert to seconds

    # Close the gif file to save memory now that we have copied out all of the frames
    gif.close()
    print("Completed Preprocessing, displaying gif\n")

    try:
        # Infinitely loop through the gif
        cur_frame = 0
        time_start = time.time()
        while (time.time() < time_start + show_time) or show_time == 0:
            if cur_frame >= num_frames:
                cur_frame = 0
            await loop.run_in_executor(None, self.matrix.SwapOnVSync, canvases[cur_frame])
            await asyncio.sleep(frame_durations[cur_frame])
            cur_frame += 1

        self.matrix.Clear()

    except asyncio.CancelledError:

        return