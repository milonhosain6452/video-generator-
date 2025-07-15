import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime

# 🔐 Token ও API Credentials
API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

app = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOADS_DIR = "downloads"
EDITED_DIR = "edited"

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(EDITED_DIR, exist_ok=True)

@app.on_message(filters.video & filters.private)
async def edit_video(client, message: Message):
    try:
        sent = await message.reply("📥 Downloading your video...")
        downloaded_path = await message.download(file_name=os.path.join(DOWNLOADS_DIR, f"{message.video.file_unique_id}.mp4"))

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = os.path.join(EDITED_DIR, f"edited_{timestamp}.mp4")

        font_path = "font.ttf"  # make sure it's in the repo

        cmd = [
            "ffmpeg",
            "-i", downloaded_path,
            "-filter_complex",
            f"[0:v]scale=720:-1,boxblur=5:1[bg];"
            f"[0:v]scale=480:-1[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,"
            f"drawtext=fontfile={font_path}:text='@viral link hub':fontcolor=white:fontsize=24:x=10:y=H-th-40,"
            f"drawtext=fontfile={font_path}:text='link on comment box / profile':fontcolor=white:fontsize=18:x=10:y=H-th-10",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y",
            output_path
        ]

        subprocess.run(cmd, check=True)
        await sent.edit("📤 Uploading edited video...")
        await message.reply_video(video=output_path, caption="✅ Edited Successfully")
        await sent.delete()

        os.remove(downloaded_path)
        os.remove(output_path)

    except Exception as e:
        await message.reply(f"❌ Error: {e}")

app.run()
