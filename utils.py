import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from PIL import Image, ImageFilter

def make_video_copyright_free(input_path, output_path, watermark_text="YourHub ©"):
    try:
        clip = VideoFileClip(input_path)
        txt_clip = TextClip(watermark_text, fontsize=40, color='white')
        txt_clip = txt_clip.set_position(("center", clip.h - 100)).set_duration(clip.duration)
        final = CompositeVideoClip([clip, txt_clip])
        final.write_videofile(output_path, codec="libx264", audio_codec="aac")
    except Exception as e:
        print("Video error:", e)

def make_image_safe(input_path, output_path):
    try:
        img = Image.open(input_path)
        img = img.filter(ImageFilter.GaussianBlur(radius=3))
        img.save(output_path)
    except Exception as e:
        print("Image error:", e)
