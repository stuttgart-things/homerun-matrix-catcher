from PIL import Image, ImageDraw, ImageFont

def create_frame(background_color, text, text_color, font_path, size):
    img = Image.new("RGB", size, background_color)
    draw = ImageDraw.Draw(img)

    if text:
        font = ImageFont.truetype(font_path, 60)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
        draw.text(position, text, fill=text_color, font=font)

    return img

# Function to generate GIF
def generate_gif(display_severity, display_system):
    font_path = "/home/sthings/homerun-matrix-catcher/fonts/Xirod.otf"
    png_path = None
    size = (400, 300)
    frames = []
    background_color = (0, 0, 0)
    system_background_color = (0, 0, 0)
    font_color = "white"

    if "ERROR" in display_severity:
        background_color = (255, 0, 0)#
        display_severity = "ERROR"
    if "SUCCESS" in display_severity:
        background_color = (0, 255, 0)
        font_color = "black"
        display_severity = "SUCCESS"
    if "INFO" in display_severity:
        background_color = (0, 0, 255)
        font_color = "black"
        display_severity = "INFO"

    if "github" in display_system:
        display_system = "GITHUB"
        system_background_color = (255, 0, 127)
        png_path = "/home/sthings/homerun-matrix-catcher/visual_aid/github.png"
    if "gitlab" in display_system:
        display_system = "GITLAB"
        system_background_color = (255, 165, 0)
        png_path = "/home/sthings/homerun-matrix-catcher/visual_aid/gitlab.png"
    if "ansible" in display_system:
        display_system = "ANSIBLE"
        system_background_color = (255, 255, 0)
    if "scale" in display_system:
        display_system = "SCALE"
        system_background_color = (255, 192, 203)

    gif_name = display_system + "_" + display_severity + ".gif"

    if png_path:
        texts_and_colors = [
            (display_severity, background_color, font_color),
            ("", (0, 0, 0), ""),
#            (display_system, system_background_color, font_color)
        ]
    else:
        texts_and_colors = [
            (display_severity, background_color, font_color),
            ("", (0, 0, 0), ""),
            (display_system, system_background_color, font_color)
        ]

    for text, bg_color, txt_color in texts_and_colors:
        frame = create_frame(bg_color, text, txt_color, font_path, size)
        frames.append(frame)
###
    if png_path:
        frame = Image.open(png_path)
        frames.append(frame)
#    else:
#        frame = create_frame(system_background_color, display_system, font_color, font_path, size)
#        frames.append(frame)
###
    base_path = "/home/sthings/homerun-matrix-catcher/visual_aid/generated/"
    gif_path = base_path + gif_name
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=[500, 1, 500],
        loop=0
    )
    print(f"GIF created: {gif_path}")
    return gif_path
