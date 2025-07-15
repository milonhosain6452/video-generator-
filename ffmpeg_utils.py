import subprocess
import os
import time

def process_video(input_path, output_path):
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-filter_complex",
        f"[0:v]scale=720:1280,boxblur=10:1[bg];"
        f"[0:v]scale=360:640[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2[vid];"
        f"[vid]drawtext=fontfile={font_path}:text='@viralLinkHub':fontcolor=white:fontsize=40:x=10:y=H-th-50,"
        f"drawtext=fontfile={font_path}:text='Link in comment box / profile':fontcolor=white:fontsize=30:x=10:y=10",
        "-filter:a", "atempo=1.05",
        "-t", "00:00:20",
        output_path
    ]

    subprocess.run(cmd)
