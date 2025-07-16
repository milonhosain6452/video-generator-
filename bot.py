from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os
import subprocess
from datetime import datetime
from keep_alive import keep_alive

# Keep Alive for Render Web Service
keep_alive()

# Telegram API credentials
API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

# Initialize the bot
app = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Constants
DOWNLOAD_DIR = "downloads"
LOGO_FILE = "logo.png"
WATERMARK_TEXT1 = "@Viral Link Hub Official"
WATERMARK_TEXT2 = "Link on Comment Box / Profile"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text(
        "🎞️ Send a video and choose what editing you want:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 Upload Video", callback_data="upload_video")]
        ])
    )

# Handle video messages
@app.on_message(filters.video & filters.private)
async def handle_video(client, message: Message):
    try:
        buttons = [
            [InlineKeyboardButton("📌 Text + Logo", callback_data=f"edit_full|{message.video.file_id}")],
            [InlineKeyboardButton("🈳 Only Logo", callback_data=f"edit_logo|{message.video.file_id}")],
            [InlineKeyboardButton("🖋️ Only Text", callback_data=f"edit_text|{message.video.file_id}")],
            [InlineKeyboardButton("🚫 No Edit", callback_data=f"edit_none|{message.video.file_id}")]
        ]
        await message.reply_text("📷 Choose what to add to your video:", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# Callback for video edit type
@app.on_callback_query()
async def callback_handler(client, callback_query):
    try:
        action, file_id = callback_query.data.split("|")
        message = callback_query.message

        await message.edit_text("📥 Downloading...")
        downloaded_path = await client.download_media(file_id, file_name=os.path.join(DOWNLOAD_DIR, "input.mp4"))

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = f"edited_{now}.mp4"

        filter_parts = [
            "[0:v]scale=720:trunc(ow/a/2)*2,boxblur=5:1[bg];",
            "[0:v]scale=480:trunc(ow/a/2)*2[fg];",
            "[bg][fg]overlay=(W-w)/2:(H-h)/2"
        ]

        if action in ["edit_full", "edit_text"]:
            filter_parts.append(
                f",drawtext=fontfile={FONT_PATH}:text='{WATERMARK_TEXT1}':fontcolor=white:fontsize=24:x=10:y=H-th-60"
            )
            filter_parts.append(
                f",drawtext=fontfile={FONT_PATH}:text='{WATERMARK_TEXT2}':fontcolor=white:fontsize=20:x=10:y=H-th-30"
            )

        if action in ["edit_full", "edit_logo"]:
            filter_parts.append(
                f",overlay=10:10:enable='between(t,0,9999)'"
            )

        command = [
            "ffmpeg", "-i", downloaded_path,
            "-i", LOGO_FILE,
            "-filter_complex", "".join(filter_parts),
            "-preset", "ultrafast", "-c:a", "aac", "-y", output_path
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(result.stderr.decode())

        await message.reply_video(output_path, caption="✅ Edited & ready!")

        os.remove(downloaded_path)
        os.remove(output_path)

    except Exception as e:
        await callback_query.message.reply_text(f"❌ Error: {e}")

app.run()
