import requests
import re
from pyrogram import filters

from BrandrdXMusic import app


@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def download_instagram_video(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ Iɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ"
        )
        return

    url = message.text.split()[1]

    if not re.match(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$", url):
        return await message.reply_text(
            "Tʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ URL ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ Iɴsᴛᴀɢʀᴀᴍ URL 😅"
        )

    a = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")

    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    try:
        response = requests.get(api_url)
        result = response.json()

        if not result["error"]:
            data = result["result"]
            video_url = data["url"]
            duration = data["duration"]
            quality = data["quality"]
            ext = data["extension"]
            size = data["formattedSize"]

            caption = f"""
Dᴜʀᴀᴛɪᴏɴ : {duration}
Qᴜᴀʟɪᴛʏ : {quality}
Tʏᴘᴇ : {ext}
Sɪᴢᴇ : {size}
"""

            await a.delete()
            await message.reply_video(video_url, caption=caption)

        else:
            await a.edit("Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇᴇʟ")

    except Exception:
        await a.edit("Eʀʀᴏʀ ᴡʜɪʟᴇ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʀᴇᴇʟ")


__MODULE__ = "Rᴇᴇʟ"

__HELP__ = """
ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ:

• /ig [URL] - ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ
• /instagram [URL] - ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ
• /reel [URL] - ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ
"""
