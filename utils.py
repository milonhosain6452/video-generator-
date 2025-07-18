import os
import uuid
import subprocess
from PIL import Image, ImageDraw, ImageFont

def make_image_safe(input_path):
    output_path = f"safe_{uuid.uuid4().hex}.jpg"
    img = Image.open(input_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not os.path.exists(font_path):
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, 40)

    text = "@YourWatermark"
    width, height = img.size
    text_width, text_height = draw.textsize(text, font=font)

    position = ((width - text_width) // 2, height - text_height - 30)
    draw.text(position, text, (255, 255, 255), font=font)

    img.save(output_path, quality=95)
    return output_path

def make_video_copyright_free(input_path):
    output_path = f"safe_{uuid.uuid4().hex}.mp4"
    watermark_text = "@YourWatermark"
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    command = [
        "ffmpeg",
        "-i", input_path,
        "-vf", f"drawtext=text='{watermark_text}':fontfile={font_path}:fontcolor=white:fontsize=36:x=(w-text_w)/2:y=(h/2)-50",
        "-codec:a", "copy",
        output_path
    ]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path
