from pyrogram import Client
from pyrogram.raw import types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from BrandrdXMusic import app


LOG_GROUP_ID = -1002150805769
LOG_CHANNEL_USERNAME = "L4inkk"


@app.on_raw_update()
async def guardian_with_log_button(client: Client, update, users, chats):

    if not isinstance(update, types.UpdateEditMessage):
        return

    msg = update.message

    if not isinstance(msg.peer_id, types.PeerChannel):
        return

    chat_id = msg.peer_id.channel_id

    if not msg.from_id:
        return

    user_id = msg.from_id.user_id
    text = msg.message or "⚠️ Media / Empty Edit"

    try:
        # 🚫 delete edited message
        await client.delete_messages(chat_id, msg.id)

        # 📌 send log to channel first
        log_msg = await client.send_message(
            LOG_GROUP_ID,
            f"""
🛡️ GROUP GUARDIAN LOG

👤 User: `{user_id}`
💬 Chat: `{chat_id}`

✏️ Edited Message:
`{text}`
"""
        )

        # 🔗 create telegram log link
        log_link = f"https://t.me/{LOG_CHANNEL_USERNAME}/{log_msg.id}"

        # 📢 group alert with button
        await client.send_message(
            chat_id,
            f"""
╔══════════════════════════╗
║  🛡️  ɢʀᴏᴜᴘ ɢᴜᴀʀᴅɪᴀɴ  🛡️  ║
╚══════════════════════════╝

⚠️ Edited Message Deleted!

👤 User : `{user_id}`
🆔 ID : `{user_id}`

━━━━━━━━━━━━━━━━━━━━━━
✏️ Edited Message:
`{text}`
━━━━━━━━━━━━━━━━━━━━━━
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔗 View Log", url=log_link)]
                ]
            )
        )

    except Exception as e:
        print("GUARDIAN BUTTON ERROR:", e)
