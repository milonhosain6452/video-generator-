import os
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from utils import make_video_copyright_free, make_image_safe

API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.photo)
async def handle_photo(client, message):
    await message.reply("📥 Downloading image...⚙️ Making it safe...")
    image = await message.download()
    safe_path = make_image_safe(image)
    await message.reply_photo(safe_path, caption="✅ Copyright-free image")

@bot.on_message(filters.video)
async def handle_video(client, message):
    await message.reply("📥 Downloading video...⚙️ Processing...")
    video = await message.download()
    output = make_video_copyright_free(video)
    await message.reply_video(output, caption="✅ Copyright-free video")

bot.run()
