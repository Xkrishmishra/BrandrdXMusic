from pyrogram import filters
from BrandrdXMusic import app
from BrandrdXMusic.misc import SUDOERS
from BrandrdXMusic.utils.database import add_off, add_on
from BrandrdXMusic.utils.decorators.language import language
import random

# Your Fixed ID
OWNER_ID = 7081885854

# English Roasts / Insults
ROAST_MESSAGES = [
    "Get lost, you piece of trash! You're not my owner.",
    "Who the hell do you think you are? Don't touch my commands!",
    "Error 404: Brain not found. Only my Master can use this.",
    "Nice try, loser! Go cry to your mom.",
    "Shut up and get out! You have no power here.",
    "Stop acting like a boss when you're just a servant. Get out!"
]

@app.on_message(filters.command(["logger", "cookies"]) & SUDOERS)
@language
async def logger(client, message, _):
    # Security Check: Only for YOU
    if message.from_user.id != OWNER_ID:
        # Send a random English roast
        roast = random.choice(ROAST_MESSAGES)
        return await message.reply_text(f"**{roast}**")

    # If it's YOU (The Owner)
    if "logger" in message.command:
        usage = _["log_1"]
        if len(message.command) != 2:
            return await message.reply_text(usage)
        
        state = message.text.split(None, 1)[1].strip().lower()
        if state == "enable":
            await add_on(2)
            await message.reply_text(_["log_2"])
        elif state == "disable":
            await add_off(2)
            await message.reply_text(_["log_3"])
        else:
            await message.reply_text(usage)
    
    # Blocked the dangerous file-sending part for safety
    elif "cookies" in message.command:
        await message.reply_text("Master, the file-leaking feature has been permanently disabled for security.")

