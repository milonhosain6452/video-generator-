import os
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import make_video_copyright_free, make_image_safe

API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

bot = Client("safe_media_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text("👋 Send me an image or video, I’ll make it copyright-free!")

@bot.on_message(filters.photo)
async def handle_photo(client, message: Message):
    sent = await message.reply_text("📥 Downloading image...⚙️ Making it safe...")
    file = await message.download()
    output_path = make_image_safe(file)
    await sent.edit("✅ Done! Here's your safe image.")
    await message.reply_photo(output_path)
    os.remove(file)
    os.remove(output_path)

@bot.on_message(filters.video)
async def handle_video(client, message: Message):
    sent = await message.reply_text("📥 Downloading video...⚙️ Processing...")
    file = await message.download()
    output_path = make_video_copyright_free(file)
    await sent.edit("✅ Done! Here's your safe video.")
    await message.reply_video(output_path)
    os.remove(file)
    os.remove(output_path)

bot.run()
