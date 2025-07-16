from pyrogram import Client, filters
from pyrogram.types import Message
import os
import subprocess
from datetime import datetime
from keep_alive import keep_alive
import re

# Keep the bot alive
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
        file_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, message.video.file_name or "input.mp4"))

        cropdetect_cmd = [
            "ffmpeg", "-i", file_path,
            "-t", "3",
            "-vf", "cropdetect",
            "-f", "null", "-"
        ]
        crop_result = subprocess.run(cropdetect_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        crop_output = crop_result.stdout.decode()
        match = re.search(r"crop=\d+:\d+:\d+:\d+", crop_output)
        crop_filter = match.group(0) if match else ""

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = f"edited_{now}.mp4"

        filter_chain = []

        if crop_filter:
            filter_chain.append(f"{crop_filter},")

        filter_chain.append(
            "scale=720:trunc(ow/a/2)*2,boxblur=5:1[bg];"
            "scale=480:trunc(ow/a/2)*2[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2[tmp];"
            f"[tmp][1:v]overlay=10:10,"
            f"drawtext=text='{TEXT_WM}':fontcolor=white:fontsize=24:x=10:y=H-th-60:box=1:boxcolor=black@0.5:boxborderw=5,"
            f"drawtext=text='{TEXT_SUB}':fontcolor=yellow:fontsize=18:x=10:y=H-th-30:box=1:boxcolor=black@0.5:boxborderw=5"
        )

        ffmpeg_command = [
            "ffmpeg", "-i", file_path,
            "-i", LOGO_PATH,
            "-filter_complex", "".join(filter_chain),
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y",
            output_path
        ]

        await message.reply_text("🎬 Editing video...")
        result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            raise Exception(result.stderr.decode())

        await message.reply_video(output_path, caption="✅ Video edited successfully!")

        os.remove(file_path)
        os.remove(output_path)

    except Exception as e:
        await message.reply_text(f"❌ Error:\n{e}")

app.run()
