import os
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app


# 🔥 NEW UPLOADER (NO ACCOUNT NEEDED)
def upload_file(file_path):
    try:
        with open(file_path, "rb") as f:
            response = requests.post("https://0x0.st", files={"file": f})

        if response.status_code == 200:
            link = response.text.strip()
            return True, link
        else:
            return False, f"Error {response.status_code}"

    except Exception as e:
        return False, str(e)


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def get_link_group(client, message):

    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a media file to convert into link!"
        )

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

        success, upload_path = upload_file(local_path)

        if success:
            await text.edit_text(
                f"✅ Uploaded Successfully!\n\n🔗 {upload_path}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Open Link",
                                url=upload_path,
                            )
                        ]
                    ]
                ),
                disable_web_page_preview=True
            )
        else:
            await text.edit_text(f"❌ Upload failed:\n{upload_path}")

    except Exception as e:
        await text.edit_text(f"❌ Error:\n{e}")

    finally:
        try:
            os.remove(local_path)
        except:
            pass
