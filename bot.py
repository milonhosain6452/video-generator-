import os 
from pyrogram 
import Client, filters from pyrogram.types import Message from editor import process_video

API_ID = 18088290 API_HASH = "1b06cbb45d19188307f10bcf275341c5" BOT_TOKEN = "7628770960:AAHKgUwOAtrolkpN4hU58ISbsZDWyIP6324"

bot = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.video & filters.private) async def handle_video(bot, message: Message): try: download_path = await message.download("downloads/") await message.reply_text("📥 ভিডিও ডাউনলোড হয়েছে, এখন এডিট হচ্ছে...")

output_path = process_video(download_path)

    await bot.send_video(
        chat_id=message.chat.id,
        video=output_path,
        caption="✅ Edited by @viralLinkHub\nLink on comment box / profile",
        supports_streaming=True
    )

    os.remove(download_path)
    os.remove(output_path)

except Exception as e:
    await message.reply_text(f"❌ এডিট করতে সমস্যা হয়েছে!\n{e}")

bot.run()
