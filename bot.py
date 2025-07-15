import os
import time
import asyncio
import subprocess
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread

# ===== API CREDENTIALS =====
API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

# ===== DOWNLOAD PATH =====
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ===== WATERMARK AND TEXT =====
WATERMARK_TEXT = "@viral link hub"
BOTTOM_TEXT = "link on comment box / profile"
FONT_PATH = "font.ttf"  # Upload OpenSans-Regular.ttf as font.ttf

# ===== BOT SETUP =====
bot = Client("video_edit_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.video & filters.private)
async def video_handler(client, message: Message):
    try:
        sent_msg = await message.reply_text("📥 Downloading video...")
        video_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, f"video_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}.mp4"))

        await sent_msg.edit("🎬 Editing video...")

        edited_path = video_path.replace(".mp4", "_edited.mp4")

        command = [
            "ffmpeg",
            "-i", video_path,
            "-filter_complex",
            f"[0:v]scale=720:-1,boxblur=5:1[bg];[0:v]scale=480:-1[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,"
            f"drawtext=fontfile={FONT_PATH}:text='{WATERMARK_TEXT}':fontcolor=white:fontsize=24:x=10:y=H-th-40,"
            f"drawtext=fontfile={FONT_PATH}:text='{BOTTOM_TEXT}':fontcolor=white:fontsize=18:x=10:y=H-th-10",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y", edited_path
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            await sent_msg.edit("❌ Error: Video editing failed.")
            print("Error:", result.stderr.decode())
            return

        await sent_msg.edit("📤 Uploading edited video...")
        await message.reply_video(edited_path, caption="✅ Edited & Copyright-Free ✅")

        await sent_msg.delete()
        os.remove(video_path)
        os.remove(edited_path)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
        print("Exception:", str(e))

# ===== FLASK SETUP FOR RENDER =====
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# ===== START BOT =====
bot.run()
