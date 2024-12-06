import asyncio
import time
from rgbmatrix import graphics

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