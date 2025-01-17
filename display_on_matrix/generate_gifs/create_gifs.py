from PIL import Image, ImageDraw, ImageFont
import imageio

# Function to create a frame with text
def create_frame(background_color, text, text_color, font_path, size):
    # Create an image with the background color
    img = Image.new("RGB", size, background_color)
    draw = ImageDraw.Draw(img)

    if text:
        # Load the font (adjust the path to a font file on your system)
        font = ImageFont.truetype(font_path, 60)  # Change size if needed

        # Calculate text position for centering
        text_bbox = draw.textbbox((0, 0), text, font=font)  # Get text bounding box
        text_width = text_bbox[2] - text_bbox[0]  # Width of text
        text_height = text_bbox[3] - text_bbox[1]  # Height of text
        position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

        # Draw the text on the image
        draw.text(position, text, fill=text_color, font=font)

    return img

# Parameters
font_path = "/home/andre/Projects/zsprechstunde/images/convertingFonts/Xirod.otf"  # Change as needed
size = (400, 300)  # Width x Height of GIF
frames = []

# Create multiple frames with different text and background colors
texts_and_colors = [
    ("SUCCESS", (0, 255, 0), "black"),   # Blue background with white text saying 'hello'
    ("", (0, 0, 0), ""),             # Black background without text
    ("ANSIBLE", (255, 255, 0), "black")  # Blue background with white text saying 'Sthings'
]

for text, bg_color, txt_color in texts_and_colors:
    frame = create_frame(bg_color, text, txt_color, font_path, size)
    frames.append(frame)

# Save as a GIF
frames[0].save(
    "/home/andre/Projects/zsprechstunde/images/created/ansible_success.gif",
    save_all=True,
    append_images=frames[1:],
    duration=[500, 1, 500],  # Duration of each frame in milliseconds
    loop=0  # Loop forever
)

print("GIF created: /created/output.gif")