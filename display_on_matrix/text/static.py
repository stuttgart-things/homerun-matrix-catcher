import asyncio
from rgbmatrix import graphics
from helper_functions.arguments import get_color, get_speed

async def static_text(self, args, ticker = True): #, loops=5, font_sytle="./spleen-32x64.bdf"):
    print("SHOWING STATIC TEXT")
    text = args.get("text")
    font_style = args.get("font", "myfont.bdf")
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