import asyncio
import os
import re

import aiofiles
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message

from aiohttp import ClientSession
from BrandrdXMusic import app
from BrandrdXMusic.utils.errors import capture_err
from BrandrdXMusic.utils.pastebin import HottyBin

pattern = re.compile(r"^text/|json$|yaml$|toml$|x-sh$|x-shellscript$")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📝  PASTE COMMAND
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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
    button = InlineKeyboard(row_width=1)
    button.add(InlineKeyboardButton(text="• ᴘᴀsᴛᴇ ʟɪɴᴋ •", url=link))
    await m.delete()
    try:
        await message.reply(
            "ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴘᴀsᴛᴇ ʟɪɴᴋ :",
            quote=False,
            reply_markup=button,
        )
    except Exception:
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🛡️  GROUP GUARDIAN — EDIT DETECTOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_edited_message(filters.group & ~filters.bot & ~filters.channel)
async def edit_watcher(_, message: Message):
    user = message.from_user
    if not user:
        return

    first = user.first_name or ""
    last = user.last_name or ""
    full_name = f"{first} {last}".strip() or "Unknown"
    mention = f"[{full_name}](tg://user?id={user.id})"

    alert = (
        "╔══════════════════════════╗\n"
        "║  🛡️  ɢʀᴏᴜᴘ ɢᴜᴀʀᴅɪᴀɴ  🛡️  ║\n"
        "╚══════════════════════════╝\n\n"
        f"⚠️  **Edited Message Detected!**\n\n"
        f"👤 **User :** {mention}\n"
        f"🆔 **User ID :** `{user.id}`\n"
        f"📝 **Action :** Message was edited\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔔 *ᴛʜɪs ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ ᴇᴅɪᴛᴇᴅ.*\n"
        "📌 *ᴛʜᴇ ᴏʀɪɢɪɴᴀʟ ᴄᴏɴᴛᴇɴᴛ ᴍᴀʏ ʜᴀᴠᴇ ᴄʜᴀɴɢᴇᴅ.*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    try:
        await message.reply(alert, quote=True)
    except Exception:
        pass
