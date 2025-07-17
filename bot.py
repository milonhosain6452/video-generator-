from pyrogram import Client, filters
from pyrogram.types import Message
import os
import subprocess
from datetime import datetime
import asyncio
from keep_alive import keep_alive

keep_alive()

API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

app = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

LOGO_PATH = "logo.png"
TEXT_WM = "@Viral Link Hub Official"
TEXT_SUB = "Link on Comment Box / Profile"

# semaphore to handle limited concurrency
sem = asyncio.Semaphore(3)  # Adjust based on load (max simultaneous video processes)

@app.on_message(filters.video & filters.private)
async def handle_video(client: Client, message: Message):
    async with sem:
        try:
            await message.reply_text("📥 Downloading your video...")
            file_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, message.video.file_name or "input.mp4"))

            now = datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = os.path.join(DOWNLOAD_DIR, f"edited_{now}.mp4")

            command = [
                "ffmpeg",
                "-i", file_path,
                "-i", LOGO_PATH,
                "-filter_complex",
                f"[0:v]scale=720:-2,crop=720:1280,boxblur=5:1[bg];"
                f"[0:v]scale=480:-2[fg];"
                f"[bg][fg]overlay=(W-w)/2:(H-h)/2[tmp];"
                f"[tmp][1:v]overlay=10:10,"
                f"drawtext=text='{TEXT_WM}':fontcolor=white:fontsize=24:x=10:y=H-th-60:box=1:boxcolor=black@0.5:boxborderw=5,"
                f"drawtext=text='{TEXT_SUB}':fontcolor=yellow:fontsize=18:x=10:y=H-th-30:box=1:boxcolor=black@0.5:boxborderw=5[v]",
                "-map", "[v]",
                "-map", "0:a?",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-c:a", "aac",
                "-y",
                output_path
            ]

            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise Exception(result.stderr.decode())

            await message.reply_video(output_path, caption="✅ Video edited successfully!")

        except Exception as e:
            await message.reply_text(f"❌ Error:\n{e}")

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(output_path):
                os.remove(output_path)

app.run()
