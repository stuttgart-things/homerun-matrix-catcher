import asyncio
from helper_functions.arguments import get_color, get_speed
from rgbmatrix import graphics

async def flow_text(self, args, ticker = True):
    text = args.get("text")
    font_style = args.get("font", "quattrocento48.bdf")
    color = get_color(args.get("color","255,192,203"))
    speed = get_speed(args.get("speed","5"))
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