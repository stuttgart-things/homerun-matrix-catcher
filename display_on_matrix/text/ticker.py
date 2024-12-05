import asyncio
from rgbmatrix import graphics

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