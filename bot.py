from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import subprocess
from datetime import datetime
from keep_alive import keep_alive

# Keep alive (Render)
keep_alive()

API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

app = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

TEXT_WM = "@Viral Link Hub Official"
TEXT_SUB = "Link on Comment Box / Profile"
LOGO_PATH = "logo.png"

user_video_map = {}

@app.on_message(filters.private & filters.video)
async def receive_video(client, message: Message):
    user_id = message.from_user.id
    user_video_map[user_id] = message.video.file_id

    buttons = [
        [InlineKeyboardButton("🎞️ Text + Logo", callback_data="edit_full")],
        [InlineKeyboardButton("🖋️ Only Text", callback_data="edit_text")],
        [InlineKeyboardButton("🖼️ Only Logo", callback_data="edit_logo")],
        [InlineKeyboardButton("🚫 No Edit", callback_data="edit_none")]
    ]

    await message.reply_text("📷 কী এডিট করতে চান ভিডিওতে?", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.private)
async def handle_callback(client, callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    await callback.answer()  # always answer callback to avoid stuck buttons

    if user_id not in user_video_map:
        await callback.message.edit_text("❌ ভিডিও পাওয়া যায়নি। দয়া করে আবার ভিডিও পাঠান।")
        return

    await callback.message.edit_text("📥 ভিডিও ডাউনলোড করা হচ্ছে...")

    try:
        input_path = await client.download_media(user_video_map[user_id], file_name=os.path.join(DOWNLOAD_DIR, f"{user_id}.mp4"))
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = f"edited_{now}.mp4"

        # FFmpeg filters
        base_filter = (
            "[0:v]scale=720:trunc(ow/a/2)*2,boxblur=5:1[bg];"
            "[0:v]scale=480:trunc(ow/a/2)*2[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2"
        )

        if data == "edit_full" or data == "edit_text":
            base_filter += (
                f",drawtext=text='{TEXT_WM}':fontcolor=white:fontsize=24:x=10:y=H-th-60,"
                f"drawtext=text='{TEXT_SUB}':fontcolor=white:fontsize=18:x=10:y=H-th-30"
            )

        ffmpeg_cmd = ["ffmpeg", "-i", input_path]

        if data in ["edit_full", "edit_logo"]:
            ffmpeg_cmd += ["-i", LOGO_PATH]
            base_filter += ",overlay=10:10"

        ffmpeg_cmd += [
            "-filter_complex", base_filter,
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y", output_path
        ]

        result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            raise Exception("FFmpeg failed:\n" + result.stderr.decode())

        await callback.message.reply_video(output_path, caption="✅ ভিডিও সফলভাবে এডিট হয়েছে!")
        os.remove(input_path)
        os.remove(output_path)

    except Exception as e:
        await callback.message.edit_text(f"❌ Error:\n{e}")
