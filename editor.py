# ✅ File: editor.py
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import os

def process_video(input_path):
    clip = VideoFileClip(input_path)
    duration = clip.duration

    # ✅ যদি ভিডিও 5 সেকেন্ডের কম হয়, তাহলে ক্লোন করে সময় বাড়ানো হবে
    if duration < 5:
        loop_count = int(6 // duration) + 1
        clips = [clip] * loop_count
        final_clip = concatenate_videoclips(clips).subclip(0, min(20, duration * loop_count))
    else:
        final_clip = clip.subclip(0, min(20, duration))

    # ✅ টেক্সট Watermark
    watermark = TextClip("@viralLinkHub", fontsize=50, color='white')
    watermark = watermark.set_position(("right", "bottom")).set_duration(final_clip.duration)

    caption = TextClip("Link on comment box / profile", fontsize=40, color='white')
    caption = caption.set_position(("center", "bottom")).set_duration(final_clip.duration)

    # ✅ Composite with watermark and text
    final = CompositeVideoClip([final_clip, watermark, caption])

    # ✅ Slight pitch and speed change (copyright protection)
    final = final.fx(lambda clip: clip.speedx(1.02))

    output_path = f"edited_{os.path.basename(input_path)}"
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path
