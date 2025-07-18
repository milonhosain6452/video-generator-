from pyrogram import Client, filters
from pyrogram.types import Message
from utils import make_video_copyright_free, make_image_safe
import os
from flask import Flask
import threading

API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

app = Flask('')
bot = Client("copyfreebot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

@bot.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply("👋 Send me any photo or video and I'll make it copyright-free!")

@bot.on_message(filters.video)
async def video_handler(client, message: Message):
    await message.reply("📥 Downloading video...")
    video_path = await message.download()
    output_path = "processed_video.mp4"
    await message.reply("⚙️ Processing...")

    make_video_copyright_free(video_path, output_path)
    await message.reply_video(output_path, caption="✅ Here's your copyright-free video")

    os.remove(video_path)
    os.remove(output_path)

@bot.on_message(filters.photo)
async def image_handler(client, message: Message):
    await message.reply("📥 Downloading image...")
    image_path = await message.download()
    await message.reply("⚙️ Making it safe...")

    output_path = make_image_safe(image_path)
    await message.reply_photo(output_path, caption="✅ Here's your copyright-free image")

    os.remove(image_path)
    os.remove(output_path)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run()
