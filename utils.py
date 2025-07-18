import os
import cv2
import uuid
import subprocess
from PIL import Image, ImageDraw, ImageFont

def make_image_safe(image_path):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    txt_layer = Image.new("RGBA", img.size, (255,255,255,0))

    draw = ImageDraw.Draw(txt_layer)
    font = ImageFont.truetype("arial.ttf", size=40)
    text = "Shared via VideoBot"
    textwidth, textheight = draw.textsize(text, font)
    x = (width - textwidth) // 2
    y = int(height * 0.88)
    draw.text((x, y), text, font=font, fill=(255,255,255,128))

    combined = Image.alpha_composite(img, txt_layer)
    output_path = f"safe_{uuid.uuid4().hex}.png"
    combined.convert("RGB").save(output_path, "PNG")
    return output_path

def make_video_copyright_free(video_path):
    output_path = f"safe_{uuid.uuid4().hex}.mp4"
    watermark = "Shared via VideoBot"
    
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"drawtext=text='{watermark}':x=(w-text_w)/2:y=h*0.85:fontcolor=white:fontsize=36:box=1:boxcolor=black@0.5",
        "-c:a", "copy", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path
