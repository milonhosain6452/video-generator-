import os 
import asyncio 
from pyrogram import Client, filters from pyrogram.types import Message from datetime import datetime import subprocess

API_ID = 28179017 API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9" BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

bot = Client("video_edit_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.video & filters.private) async def edit_video(client: Client, message: Message): try: sent_msg = await message.reply_text("⏳ Downloading video...")

file_path = await message.download(file_name="downloads/edited_input.mp4")
    edited_file = f"edited_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"

    cmd = [
        'ffmpeg', '-i', file_path,
        '-filter_complex',
        "[0:v]scale=720:-1,boxblur=5:1[bg];"
        "[0:v]scale=480:-1[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2," 
        "drawtext=fontfile=font.ttf:text='@viral link hub':fontcolor=white:fontsize=24:x=10:y=H-th-40," 
        "drawtext=fontfile=font.ttf:text='link on comment box / profile':fontcolor=white:fontsize=18:x=10:y=H-th-10",
        '-preset', 'ultrafast', '-c:a', 'aac', '-y', edited_file
    ]

    await sent_msg.edit("🎞️ Editing video...")
    subprocess.run(cmd, check=True)

    await message.reply_video(edited_file, caption="✅ Edited & Copyright-Free Video")
    await sent_msg.delete()

    os.remove(file_path)
    os.remove(edited_file)
except Exception as e:
    await message.reply_text(f"❌ Error: {e}")

if name == 'main': bot.run()
