from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import subprocess
from datetime import datetime
from keep_alive import keep_alive

# Keep the bot alive (Render/Replit)
keep_alive()

# Telegram API credentials
API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

# Initialize bot
app = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Constants
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
LOGO_PATH = "logo.png"
TEXT_WM = "@Viral Link Hub Official"
TEXT_SUB = "Link on Comment Box / Profile"

# Store file_ids mapped to user IDs
file_id_map = {}

# Step 1: Receive video and ask for edit type
@app.on_message(filters.video & filters.private)
async def handle_video(client: Client, message: Message):
    try:
        file_id_map[message.from_user.id] = message.video.file_id

        buttons = [
            [InlineKeyboardButton("🎞️ Text + Logo", callback_data="edit_full")],
            [InlineKeyboardButton("🈳 Only Logo", callback_data="edit_logo")],
            [InlineKeyboardButton("🖋️ Only Text", callback_data="edit_text")],
            [InlineKeyboardButton("🚫 No Edit", callback_data="edit_none")]
        ]
        await message.reply_text("📷 Choose what to add to your video:", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# Step 2: Handle button selection
@app.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    action = callback_query.data
    user_id = callback_query.from_user.id
    message = callback_query.message

    if user_id not in file_id_map:
        await message.edit_text("❌ Video not found. Please send it again.")
        return

    file_id = file_id_map[user_id]
    await message.edit_text("📥 Downloading your video...")

    try:
        # Download video from Telegram
        downloaded_path = await client.download_media(file_id, file_name=os.path.join(DOWNLOAD_DIR, f"{user_id}.mp4"))
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = f"edited_{now}.mp4"

        # Build FFmpeg filter
        filters_list = [
            "[0:v]scale=720:trunc(ow/a/2)*2,boxblur=5:1[bg];",
            "[0:v]scale=480:trunc(ow/a/2)*2[fg];",
            "[bg][fg]overlay=(W-w)/2:(H-h)/2"
        ]

        if action in ["edit_full", "edit_text"]:
            filters_list.append(
                f",drawtext=text='{TEXT_WM}':fontcolor=white:fontsize=24:x=10:y=H-th-60"
                f",drawtext=text='{TEXT_SUB}':fontcolor=white:fontsize=18:x=10:y=H-th-30"
            )

        if action in ["edit_full", "edit_logo"]:
            filters_list.append(f",overlay=10:10:enable='between(t,0,20)' [out]")

        ffmpeg_cmd = [
            "ffmpeg", "-i", downloaded_path
        ]

        # Add logo if needed
        if action in ["edit_full", "edit_logo"]:
            ffmpeg_cmd += ["-i", LOGO_PATH]

        ffmpeg_cmd += [
            "-filter_complex", "".join(filters_list),
            "-map", "[out]" if "edit_logo" in action else "0:v",
            "-map", "0:a?",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y", output_path
        ]

        result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            raise Exception("FFmpeg failed:\n" + result.stderr.decode())

        await message.reply_video(output_path, caption="✅ Video edited successfully!")

        os.remove(downloaded_path)
        os.remove(output_path)

    except Exception as e:
        await message.edit_text(f"❌ Error: Video editing failed.\n\n{e}")
