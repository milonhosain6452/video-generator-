import os
import asyncio
import subprocess
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading

API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"
USER_ID = 5363534043

# Flask app to keep service alive
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running on Render!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()

bot = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.video & filters.private)
async def handle_video(client, message: Message):
    if message.from_user.id != USER_ID:
        await message.reply_text("⛔️ Permission denied.")
        return

    status = await message.reply_text("⬇️ Downloading...")
    input_path = await message.download()
    output_path = f"edited_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"

    await status.edit("🎬 Editing...")

    command = [
        "ffmpeg",
        "-i", input_path,
        "-filter_complex",
        "[0:v]scale=720:-1,boxblur=5:1[bg];"
        "[0:v]scale=480:-1[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2,"
        "drawtext=text='@viral link hub':fontcolor=white:fontsize=24:x=10:y=H-th-40,"
        "drawtext=text='link on comment box / profile':fontcolor=white:fontsize=18:x=10:y=H-th-10",
        "-preset", "ultrafast",
        "-c:a", "aac",
        "-y", output_path
    ]

    try:
        subprocess.run(command, check=True)
        await status.edit("⬆️ Uploading...")
        await message.reply_video(video=output_path, caption="✅ Edited by @YourBot")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
    finally:
        await status.delete()
        os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

bot.run()
