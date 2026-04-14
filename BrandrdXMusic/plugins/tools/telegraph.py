import os
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app

# 🔥 YOUR PRIVATE CHANNEL ID
CHANNEL_ID = -1002387986267


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def get_link_group(client, message):

    if not message.reply_to_message:
        return await message.reply_text("Reply to a media file!")

    media = message.reply_to_message

    text = await message.reply("📥 Downloading...")

    async def progress(current, total):
        try:
            await text.edit_text(f"📥 Downloading... {current * 100 / total:.1f}%")
        except:
            pass

    try:
        # Download file
        local_path = await media.download(progress=progress)

        await text.edit_text("📤 Uploading to Telegram...")

        # Upload to channel
        sent = await app.send_document(CHANNEL_ID, local_path)

        # Generate link
        if sent.chat.username:
            link = f"https://t.me/{sent.chat.username}/{sent.id}"
        else:
            link = f"https://t.me/c/{str(CHANNEL_ID)[4:]}/{sent.id}"

        await text.edit_text(
            f"✅ Uploaded Successfully!\n\n🔗 {link}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open Link", url=link)]]
            ),
            disable_web_page_preview=True
        )

    except Exception as e:
        await text.edit_text(f"❌ Error:\n{e}")

    finally:
        try:
            os.remove(local_path)
        except:
            pass
