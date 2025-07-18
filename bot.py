import os
from pyrogram import Client, filters
from utils import make_video_copyright_free, make_image_safe
from pyrogram.types import Message

API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

bot = Client("copyright_free_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    await message.reply("👋 Send me any image or video, I'll make it copyright-free with watermark!")

@bot.on_message(filters.photo)
async def handle_photo(client, message: Message):
    m = await message.reply("📥 Downloading image...⚙️ Making it safe...")
    path = await message.download()
    safe_path = make_image_safe(path)
    await m.edit("✅ Done! Sending...")
    await message.reply_photo(safe_path, caption="✅ Copyright-free image")
    os.remove(path)
    os.remove(safe_path)

@bot.on_message(filters.video)
async def handle_video(client, message: Message):
    m = await message.reply("📥 Downloading video...⚙️ Processing...")
    path = await message.download()
    out_path = make_video_copyright_free(path)
    await m.edit("✅ Done! Sending...")
    await message.reply_video(out_path, caption="✅ Copyright-free video")
    os.remove(path)
    os.remove(out_path)

bot.run()
