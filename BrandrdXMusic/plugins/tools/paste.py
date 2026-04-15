import asyncio
import os
import re

import aiofiles
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.raw import types
from aiohttp import ClientSession

from BrandrdXMusic import app
from BrandrdXMusic.utils.errors import capture_err
from BrandrdXMusic.utils.pastebin import HottyBin


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⚙️ LOG SETTINGS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LOG_GROUP_ID = -1002150805769   # 🔴 PUT YOUR LOG CHANNEL ID
LOG_CHANNEL_USERNAME = "L4inkk"  # 🔴 WITHOUT @


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📝 PASTE COMMAND
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

pattern = re.compile(r"^text/|json$|yaml$|toml$|x-sh$|x-shellscript$")

async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with ClientSession() as session:
                async with session.head(preview, timeout=2) as resp:
                    status = resp.status
                    size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return True if status == 200 else False
    return False


@app.on_message(filters.command("paste"))
@capture_err
async def paste_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message With /paste")

    m = await message.reply_text("Pasting...")

    if message.reply_to_message.text:
        content = str(message.reply_to_message.text)

    elif message.reply_to_message.document:
        document = message.reply_to_message.document

        if document.file_size > 1048576:
            return await m.edit("You can only paste files smaller than 1MB.")

        if not pattern.search(document.mime_type):
            return await m.edit("Only text files can be pasted.")

        doc = await message.reply_to_message.download()

        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()

        os.remove(doc)

    else:
        return await m.edit("Nothing to paste.")

    link = await HottyBin(content)

    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴘᴀsᴛᴇ ʟɪɴᴋ •", url=link)]
    ])

    await m.delete()

    try:
        await message.reply(
            "ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴘᴀsᴛᴇ ʟɪɴᴋ :",
            quote=False,
            reply_markup=button,
        )
    except:
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🛡️ RAW EDIT GUARDIAN (WORKS EVERYWHERE)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_raw_update()
async def raw_edit_handler(client: Client, update, users, chats):

    if not isinstance(update, types.UpdateEditMessage):
        return

    message = update.message

    # ✅ Only handle supergroups
    if not isinstance(message.peer_id, types.PeerChannel):
        return

    chat_id = message.peer_id.channel_id

    # ❌ Ignore if no sender
    if not message.from_id or not hasattr(message.from_id, "user_id"):
        return

    user_id = message.from_id.user_id
    text = message.message

    if not text:
        return

    try:
        # 🧹 DELETE MESSAGE
        await client.delete_messages(chat_id, message.id)

        # 📂 SEND LOG
        log_msg = await client.send_message(
            LOG_GROUP_ID,
            f"🛡️ **Edit Log**\n\n"
            f"👤 User ID: `{user_id}`\n"
            f"💬 Chat ID: `{chat_id}`\n\n"
            f"✏️ Edited Message:\n`{text}`"
        )

        # 🔗 CREATE LINK
        log_link = f"https://t.me/{LOG_CHANNEL_USERNAME}/{log_msg.id}"

        # 📢 SEND ALERT IN GROUP
        await client.send_message(
            chat_id,
            f"⚠️ **Edited Message Deleted!**\n\n"
            f"👤 User ID: `{user_id}`\n\n"
            f"✏️ Message:\n`{text}`\n\n"
            f"🔗 [View Log]({log_link})",
            disable_web_page_preview=True
        )

    except Exception as e:
        print("RAW ERROR:", e)
