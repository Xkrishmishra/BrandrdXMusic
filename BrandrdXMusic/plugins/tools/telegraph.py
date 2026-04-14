import os
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app


# 🔥 UPLOADERS

def upload_0x0(file_path):
    try:
        with open(file_path, "rb") as f:
            r = requests.post("https://0x0.st", files={"file": f})
        if r.status_code == 200:
            return True, r.text.strip()
        return False, "0x0 failed"
    except Exception:
        return False, "0x0 error"


def upload_transfer(file_path):
    try:
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            r = requests.put(f"https://transfer.sh/{filename}", data=f)
        if r.status_code == 200:
            return True, r.text.strip()
        return False, "transfer failed"
    except Exception:
        return False, "transfer error"


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def get_link_group(client, message):

    if not message.reply_to_message:
        return await message.reply_text("Reply to a media file!")

    media = message.reply_to_message

    file_size = 0
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size

    if file_size > 200 * 1024 * 1024:
        return await message.reply_text("File must be under 200MB!")

    text = await message.reply("📥 Downloading...")

    async def progress(current, total):
        try:
            await text.edit_text(f"📥 Downloading... {current * 100 / total:.1f}%")
        except:
            pass

    try:
        local_path = await media.download(progress=progress)

        await text.edit_text("📤 Uploading...")

        # 🔥 TRY 0x0
        success, link = upload_0x0(local_path)

        # 🔁 FALLBACK → transfer.sh
        if not success:
            await text.edit_text("⚠️ Switching server...")
            success, link = upload_transfer(local_path)

        if success:
            await text.edit_text(
                f"✅ Uploaded Successfully!\n\n🔗 {link}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Open Link", url=link)]]
                ),
                disable_web_page_preview=True
            )
        else:
            await text.edit_text("❌ All upload servers failed!")

    except Exception as e:
        await text.edit_text(f"❌ Error:\n{e}")

    finally:
        try:
            os.remove(local_path)
        except:
            pass
