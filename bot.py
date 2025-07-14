import os
import time
from pyrogram import Client, filters
from editor import process_video

API_ID = 18088290
API_HASH = "1b06cbb45d19188307f10bcf275341c5"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

bot = Client("editor-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@bot.on_message(filters.video)
async def handle_video(client, message):
    try:
        await message.reply("📥 ভিডিও ডাউনলোড হচ্ছে...")
        video_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, f"{int(time.time())}.mp4"))

        output_path = f"edited_{os.path.basename(video_path)}"
        await message.reply("🎬 ভিডিও প্রসেস হচ্ছে...")

        process_video(video_path, output_path)

        await message.reply_video(output_path, caption="✅ Done! Edited & Ready 🎞️")

        os.remove(video_path)
        os.remove(output_path)

    except Exception as e:
        await message.reply(f"❌ এডিট করতে সমস্যা হয়েছে!\nError: {e}")

bot.run()
