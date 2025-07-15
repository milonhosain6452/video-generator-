from pyrogram import Client, filters
from pyrogram.types import Message
import os
import subprocess
from datetime import datetime
from keep_alive import keep_alive

# Keep the bot alive (for Render web service)
keep_alive()

# Telegram API credentials
API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

# Initialize the bot
app = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Create downloads directory
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.on_message(filters.video & filters.private)
async def handle_video(client: Client, message: Message):
    try:
        await message.reply_text("📥 Downloading your video...")
        downloaded_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, message.video.file_name or "input.mp4"))

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = f"edited_{now}.mp4"

        command = [
            "ffmpeg",
            "-i", downloaded_path,
            "-filter_complex",
            "[0:v]scale=720:trunc(ow/a/2)*2,boxblur=5:1[bg];"
            "[0:v]scale=480:trunc(ow/a/2)*2[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y",
            output_path
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            raise Exception("FFmpeg failed:\n" + result.stderr.decode())

        await message.reply_video(output_path, caption="✅ Video edited successfully!")

        os.remove(downloaded_path)
        os.remove(output_path)

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

app.run()
