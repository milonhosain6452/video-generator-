import ffmpeg
from PIL import Image, ImageDraw, ImageFont
import os

# ভিডিও কপিরাইট ফ্রি করে, watermark + text বসিয়ে
def make_video_copyright_free(input_path, output_path):
    watermark_text = "YourBot | CopyFree"
    watermark_logo = "logo.png"  # এই ফাইলটা প্রজেক্টে থাকতে হবে

    # মিডল নিচে লেখা বসানো (text)
    ffmpeg.input(input_path).output(
        output_path,
        vf=f"drawtext=text='{watermark_text}':x=(w-text_w)/2:y=h-th-80:fontsize=30:fontcolor=white:borderw=2,"
           f"movie={watermark_logo}[wm];[in][wm]overlay=W-w-10:H-h-10",
        codec="libx264", acodec="copy", strict="-2"
    ).run(overwrite_output=True)

# ইমেজ কপিরাইট ফ্রি করার জন্য blur + logo + text
def make_image_safe(image_path):
    base = Image.open(image_path).convert("RGBA").resize((512, 512))
    txt = Image.new('RGBA', base.size, (255,255,255,0))

    # Text watermark
    font = ImageFont.truetype("arial.ttf", 24)
    d = ImageDraw.Draw(txt)
    d.text((10, 10), "YourBot | CopyFree", font=font, fill=(255,255,255,128))

    # Overlay logo
    if os.path.exists("logo.png"):
        logo = Image.open("logo.png").resize((80, 80))
        base.paste(logo, (base.size[0]-90, base.size[1]-90), logo)

    watermarked = Image.alpha_composite(base, txt)
    final_path = "processed_image.png"
    watermarked.save(final_path)
    return final_path
