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

# Create download directory if not exists
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Watermark texts
WATERMARK = "@viral link hub"
SUBTEXT = "link on comment box / profile"

# Font file
FONT_FILE = "font.ttf"  # Make sure this file exists

# Handle video messages
@app.on_message(filters.video & filters.private)
async def handle_video(client: Client, message: Message):
    try:
        await message.reply_text("📥 Downloading your video...")
        safe_filename = message.video.file_name or f"video_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
        downloaded_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, safe_filename))

        # Generate edited file name
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = f"edited_{now}.mp4"

        # FFmpeg command
        command = [
            "ffmpeg",
            "-i", downloaded_path,
            "-filter_complex",
            f"[0:v]scale=720:-1,boxblur=5:1[bg];[0:v]scale=480:-1[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,"
            f"drawtext=fontfile={FONT_FILE}:text='{WATERMARK}':fontcolor=white:fontsize=24:x=10:y=H-th-40,"
            f"drawtext=fontfile={FONT_FILE}:text='{SUBTEXT}':fontcolor=white:fontsize=18:x=10:y=H-th-10",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y",
            output_path
        ]

        # Run FFmpeg
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            raise Exception("FFmpeg failed:\n" + result.stderr.decode())

        await message.reply_video(output_path, caption="✅ Edited & ready to share!")

        os.remove(downloaded_path)
        os.remove(output_path)

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# Run the bot
app.run()
