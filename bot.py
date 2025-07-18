import os
from pyrogram import Client, filters
from utils import make_video_copyright_free, make_image_safe
from flask_app import app
import threading

API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

bot = Client("cfbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.video | filters.document.video)
async def handle_video(_, msg):
    sent = await msg.reply("⏳ ভিডিও প্রসেস হচ্ছে...")
    try:
        path = await msg.download()
        out_path = "edited_" + path
        make_video_copyright_free(path, out_path)
        await msg.reply_video(out_path, caption="✅ কপিরাইট ফ্রি করা হলো!")
        await sent.delete()
        os.remove(path)
        os.remove(out_path)
    except Exception as e:
        await sent.edit(f"❌ ভিডিও এডিটে সমস্যা: {e}")

@bot.on_message(filters.photo)
async def handle_photo(_, msg):
    sent = await msg.reply("🖼️ ইমেজ প্রসেস হচ্ছে...")
    try:
        path = await msg.download()
        out_path = "edited_" + path
        make_image_safe(path, out_path)
        await msg.reply_photo(out_path, caption="✅ ইমেজ ক্লিন করা হলো!")
        await sent.delete()
        os.remove(path)
        os.remove(out_path)
    except Exception as e:
        await sent.edit(f"❌ ইমেজ প্রসেসে সমস্যা: {e}")

@bot.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("👋 Just send a video or photo, I’ll edit it to be copyright-free!")

def run():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run).start()
    bot.run()
