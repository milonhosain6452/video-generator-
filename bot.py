import os
from pyrogram import Client, filters
from ffmpeg_utils import process_video

API_ID = 18088290
API_HASH = "1b06cbb45d19188307f10bcf275341c5"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

app = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOADS = "./downloads"
os.makedirs(DOWNLOADS, exist_ok=True)

@app.on_message(filters.video & filters.private)
async def handle_video(client, message):
    sent_msg = await message.reply("📥 Downloading video...")
    video_path = await message.download(file_name=os.path.join(DOWNLOADS, "input.mp4"))
    
    await sent_msg.edit("🎬 Editing video...")
    output_path = os.path.join(DOWNLOADS, f"edited_{int(time.time())}.mp4")
    process_video(video_path, output_path)

    await sent_msg.edit("📤 Sending final video...")
    await message.reply_video(video=output_path, caption="Here is your edited video!")
    await sent_msg.delete()

app.run()
