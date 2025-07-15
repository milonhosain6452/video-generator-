import os
import time
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
import subprocess

API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

app = Client("video_generator_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO)

def edit_video(input_file, output_file):
    try:
        command = [
            "ffmpeg",
            "-i", input_file,
            "-filter_complex",
            "[0:v]scale=720:-1,boxblur=5:1[bg];[0:v]scale=480:-1[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,"
            "drawtext=text='@viral link hub':fontcolor=white:fontsize=24:x=10:y=H-th-40,"
            "atempo=1.1",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y", output_file
        ]
        subprocess.run(command, check=True)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

@app.on_message(filters.video)
async def handle_video(client, message: Message):
    sent_msg = await message.reply("📥 Downloading...")
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        video_path = os.path.join(DOWNLOAD_FOLDER, f"video_{timestamp}.mp4")
        edited_path = f"edited_{timestamp}.mp4"

        await message.download(video_path)
        await sent_msg.edit("🎞️ Editing...")

        # Check duration
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            capture_output=True, text=True
        )
        duration = float(probe.stdout.strip())

        if duration < 5:
            loops = int(7 // duration) + 1
            loop_path = f"looped_{timestamp}.mp4"
            subprocess.run([
                "ffmpeg", "-stream_loop", str(loops), "-i", video_path,
                "-t", "7", "-c", "copy", loop_path
            ], check=True)
            os.remove(video_path)
            video_path = loop_path

        if edit_video(video_path, edited_path):
            await sent_msg.edit("📤 Sending edited video...")
            await message.reply_video(edited_path)
            await sent_msg.delete()
        else:
            await sent_msg.edit("❌ Error: Video editing failed.")
    except Exception as e:
        await sent_msg.edit(f"❌ Error: {e}")

app.run()
