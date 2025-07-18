import os
from pyrogram import Client, filters
from pyrogram.types import Message
import subprocess
import asyncio
from flask import Flask
import threading

# ========== API CONFIG ==========
API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

# ========== LOGO / TEXT ==========
WATERMARK_TEXT = "© YourBrand"
LOGO_FILE = "logo.png"  # optional, keep in same folder

# ========== FLASK APP ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()

# ========== TELEGRAM BOT ==========
bot = Client(
    "watermark_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ===== Image Watermark (Text only) =====
async def process_image(input_path, output_path):
    cmd = [
        "ffmpeg", "-i", input_path,
        "-vf", f"drawtext=text='{WATERMARK_TEXT}':fontcolor=white:fontsize=30:x=10:y=H-th-10",
        "-y", output_path
    ]
    subprocess.run(cmd)

# ===== Video Watermark (Text only) =====
async def process_video(input_path, output_path):
    cmd = [
        "ffmpeg", "-i", input_path,
        "-vf", f"drawtext=text='{WATERMARK_TEXT}':fontcolor=white:fontsize=24:x=10:y=H-th-10",
        "-c:a", "copy",
        "-y", output_path
    ]
    subprocess.run(cmd)

# ====== Image Handler ======
@bot.on_message(filters.photo)
async def image_handler(client, message: Message):
    msg = await message.reply("🔄 Processing image...")
    downloaded = await message.download()
    output = "processed_image.jpg"
    await process_image(downloaded, output)
    await message.reply_photo(photo=output, caption="✅ Done with watermark.")
    await msg.delete()
    os.remove(downloaded)
    os.remove(output)

# ====== Video Handler ======
@bot.on_message(filters.video)
async def video_handler(client, message: Message):
    msg = await message.reply("🔄 Processing video...")
    downloaded = await message.download()
    output = "processed_video.mp4"
    await process_video(downloaded, output)
    await message.reply_video(video=output, caption="✅ Watermark added.")
    await msg.delete()
    os.remove(downloaded)
    os.remove(output)

# ====== Start Command ======
@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply("👋 Send me a photo or video and I’ll watermark it!")

# ===== MAIN =====
keep_alive()

if __name__ == "__main__":
    bot.run()
