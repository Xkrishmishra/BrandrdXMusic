import os
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app

# ✅ YOUR CHANNEL ID
CHANNEL_ID = -1002150805769


# 🌐 1. CATBOX
def upload_catbox(file_path):
    try:
        with open(file_path, "rb") as f:
            r = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": f}
            )
        if r.status_code == 200 and r.text.startswith("http"):
            return True, r.text.strip()
        return False, "Catbox failed"
    except:
        return False, "Catbox error"


# 🌐 2. 0x0
def upload_0x0(file_path):
    try:
        with open(file_path, "rb") as f:
            r = requests.post("https://0x0.st", files={"file": f})
        if r.status_code == 200:
            return True, r.text.strip()
        return False, "0x0 failed"
    except:
        return False, "0x0 error"


# 🌐 3. transfer.sh
def upload_transfer(file_path):
    try:
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            r = requests.put(f"https://transfer.sh/{filename}", data=f)
        if r.status_code == 200:
            return True, r.text.strip()
        return False, "transfer failed"
    except:
        return False, "transfer error"


# 📦 4. TELEGRAM (FINAL)
async def upload_telegram(file_path):
    try:
        sent = await app.send_document(CHANNEL_ID, file_path)

        if sent.chat.username:
            link = f"https://t.me/{sent.chat.username}/{sent.id}"
        else:
            link = f"https://t.me/c/{str(CHANNEL_ID)[4:]}/{sent.id}"

        return True, link
    except Exception as e:
        return False, str(e)


# 🚀 MAIN COMMAND
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

        # 🔥 1. CATBOX
        await text.edit_text("📤 Uploading → Catbox...")
        success, link = upload_catbox(local_path)
        source = "Catbox"

        # 🔁 2. 0x0
        if not success:
            await text.edit_text("⚠️ Catbox failed → 0x0...")
            success, link = upload_0x0(local_path)
            source = "0x0"

        # 🔁 3. transfer.sh
        if not success:
            await text.edit_text("⚠️ 0x0 failed → Transfer...")
            success, link = upload_transfer(local_path)
            source = "Transfer.sh"

        # 🔁 4. Telegram
        if not success:
            await text.edit_text("⚠️ All failed → Telegram backup...")
            success, link = await upload_telegram(local_path)
            source = "Telegram"

        # ✅ FINAL RESULT
        if success:
            await text.edit_text(
                f"✅ Uploaded Successfully!\n\n"
                f"📡 Source: {source}\n"
                f"🔗 Link: {link}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Open Link", url=link)]]
                ),
                disable_web_page_preview=True
            )
        else:
            await text.edit_text("❌ All upload methods failed!")

    except Exception as e:
        await text.edit_text(f"❌ Error:\n{e}")

    finally:
        try:
            os.remove(local_path)
        except:
            pass
