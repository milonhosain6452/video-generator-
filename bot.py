from pyrogram import Client, filters
from pyrogram.types import Message
import os
import subprocess
from datetime import datetime
from keep_alive import keep_alive

keep_alive()

API_ID = 28179017
API_HASH = "3eccbcc092d1a95e5c633913bfe0d9e9"
BOT_TOKEN = "8194588818:AAHmvjJ42eR_VoGHXzxzqPfvMi8eJ9_OsAc"

app = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

LOGO_PATH = "logo.png"
TEXT_WM = "@Viral Link Hub Official"
TEXT_SUB = "Link on Comment Box / Profile"

@app.on_message(filters.video & filters.private)
async def handle_video(client: Client, message: Message):
    try:
        await message.reply_text("📥 Downloading your video...")

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        input_filename = f"{message.video.file_unique_id}_{now}.mp4"
        file_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, input_filename))
        output_path = os.path.join(DOWNLOAD_DIR, f"edited_{now}.mp4")

        command = [
            "ffmpeg",
            "-i", file_path,
            "-i", LOGO_PATH,
            "-filter_complex",
            f"[0:v]crop=iw-40:ih-40:20:20,scale=720:trunc(ow/a/2)*2,boxblur=5:1[bg];"
            f"[0:v]crop=iw-40:ih-40:20:20,scale=480:trunc(ow/a/2)*2[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2[tmp];"
            f"[tmp][1:v]overlay=10:10,"
            f"drawtext=text='{TEXT_WM}':fontcolor=white:fontsize=24:x=10:y=H/2+100:box=1:boxcolor=black@0.5:boxborderw=5,"
            f"drawtext=text='{TEXT_SUB}':fontcolor=yellow:fontsize=18:x=10:y=H/2+140:box=1:boxcolor=black@0.5:boxborderw=5[v]",
            "-map", "[v]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y",
            output_path
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(result.stderr.decode())

        await message.reply_video(output_path, caption="✅ Video edited successfully!")

    except Exception as e:
        await message.reply_text(f"❌ Error:\n{e}")

    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        except Exception as cleanup_err:
            print(f"Cleanup Error: {cleanup_err}")

# 🖼️ Handle Image with Watermark/Text (for missav-type uploads)
@app.on_message(filters.photo & filters.private)
async def handle_photo(client: Client, message: Message):
    try:
        await message.reply_text("🖼️ Processing image...")

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        input_file = os.path.join(DOWNLOAD_DIR, f"photo_{now}.jpg")
        output_file = os.path.join(DOWNLOAD_DIR, f"watermarked_{now}.jpg")
        await message.download(file_name=input_file)

        # Add watermark text
        command = [
            "ffmpeg",
            "-i", input_file,
            "-i", LOGO_PATH,
            "-filter_complex",
            f"overlay=10:10,"
            f"drawtext=text='{TEXT_WM}':fontcolor=white:fontsize=32:x=10:y=H/2-40:box=1:boxcolor=black@0.5:boxborderw=4,"
            f"drawtext=text='{TEXT_SUB}':fontcolor=yellow:fontsize=24:x=10:y=H/2:box=1:boxcolor=black@0.5:boxborderw=4",
            "-y",
            output_file
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(result.stderr.decode())

        await message.reply_photo(output_file, caption="✅ Image processed!")

    except Exception as e:
        await message.reply_text(f"❌ Error processing image:\n{e}")

    finally:
        try:
            if os.path.exists(input_file):
                os.remove(input_file)
            if os.path.exists(output_file):
                os.remove(output_file)
        except Exception as cleanup_err:
            print(f"Cleanup Error: {cleanup_err}")

# Run the bot
app.run()
