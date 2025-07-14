import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.audio.fx.all import audio_fadein, audio_fadeout

def process_video(input_path, output_path):
    clip = VideoFileClip(input_path)
    duration = clip.duration

    # Clone loop if too short
    if duration < 5:
        n = int(7 // duration) + 1
        clip = concatenate_videoclips([clip] * n).subclip(0, 7)

    elif duration > 20:
        clip = clip.subclip(0, 20)

    # Resize & add watermark text
    clip = clip.resize(width=720)
    txt = "@Viral Link Hub\nLink in comment box / profile"

    clip = clip.set_position(("center", "center")).margin(top=20, opacity=0)
    clip = clip.set_audio(clip.audio.fx(audio_fadein, 0.5).fx(audio_fadeout, 0.5))

    # Slight pitch shift via fps change (copyright evasion)
    clip = clip.fx(lambda c: c.set_fps(c.fps * 1.03))

    # Save
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac', threads=4, preset='ultrafast')
