import os
import uuid
import subprocess
from PIL import Image, ImageDraw, ImageFont

def make_image_safe(input_path):
    output_path = f"safe_{uuid.uuid4().hex[:6]}.jpg"
    image = Image.open(input_path).convert("RGB")

    # Blur
    image = image.resize((image.width//2, image.height//2)).resize((image.width, image.height))

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
    text = "YourBrand"
    draw.text((10, 10), text, font=font, fill=(255, 255, 255))

    image.save(output_path, "JPEG")
    return output_path

def make_video_copyright_free(input_path):
    output_path = f"safe_{uuid.uuid4().hex[:6]}.mp4"
    watermark_path = "logo.png"
    text = "YourBrand"

    command = [
        "ffmpeg", "-i", input_path,
        "-i", watermark_path,
        "-filter_complex",
        "[0:v][1:v] overlay=W-w-10:H-h-60,drawtext=text='{}':x=(w-text_w)/2:y=h-100:fontsize=24:fontcolor=white:shadowcolor=black:shadowx=2:shadowy=2".format(text),
        "-c:a", "copy", output_path
    ]
    subprocess.run(command)
    return output_path
