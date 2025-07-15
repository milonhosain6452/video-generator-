# ✅ bot.py
import os
from pyrogram import Client, filters
from editor import process_video

# Bot Config
API_ID = 18088290
API_HASH = "1b06cbb45d19188307f10bcf275341c5"
BOT_TOKEN = "7628770960:AAHKgUwOAtrolkpN4hU58ISbsZDWyIP6324"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.on_message(filters.video & filters.private)
async def handle_video(client, message):
    video = message.video
    file_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, f"{message.id}.mp4"))
    await message.reply_text("✅ ভিডিও ডাউনলোড শেষ। এখন এডিট হচ্ছে...")

    try:
        edited_path = process_video(file_path)
        await message.reply_video(video=edited_path, caption="✅ Done! @viralLinkHub")
        os.remove(edited_path)
        os.remove(file_path)
    except Exception as e:
        await message.reply_text(f"❌ এডিটিংয়ে সমস্যা: {e}")

app.run()
