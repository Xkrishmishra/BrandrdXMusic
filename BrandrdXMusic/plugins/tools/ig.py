import os
import re
import asyncio
import yt_dlp
from pyrogram import filters
from BrandrdXMusic import app

# Ensure download directory exists
DOWNLOAD_DIR = 'downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_video(url):
    """Synchronous function to handle yt-dlp download"""
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def download_instagram_video(client, message):
    # 1. Validate Command Input
    if len(message.command) < 2:
        return await message.reply_text(
            "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ Iɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ"
        )

    url = message.text.split(None, 1)[1]

    # 2. Validate URL Format
    if not re.match(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$", url):
        return await message.reply_text(
            "Tʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ URL ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ Iɴsᴛᴀɢʀᴀᴍ URL 😅"
        )

    # 3. Status Update
    status = await message.reply_text("⏳ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ʀᴇᴇʟ...")

    try:
        # 4. Download (Running blocking code in executor)
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, download_video, url)

        # 5. Send Video
        await status.edit("📤 ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ...")
        await message.reply_video(
            video=file_path,
            caption="✅ **Dᴏᴡɴʟᴏᴀᴅ Cᴏᴍᴘʟᴇᴛᴇᴅ!**"
        )

        # 6. Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
        await status.delete()

    except Exception as e:
        await status.edit(f"❌ **Eʀʀᴏʀ:** {str(e)}")

__MODULE__ = "Rᴇᴇʟ"

__HELP__ = """
ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ:

• /ig [URL] - ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ
• /instagram [URL] - ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ
• /reel [URL] - ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ
"""
