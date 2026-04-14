import math
from pyrogram.types import InlineKeyboardButton
from BrandrdXMusic.utils.formatters import time_to_seconds


# ──────────────────────────────────────────────────────
#  🎧 MINIMAL FONT (clean + safe)
# ──────────────────────────────────────────────────────

def _mono(text: str) -> str:
    return ''.join(chr(0x1D7F6 + ord(c) - 48) if c.isdigit() else c for c in text)


# ──────────────────────────────────────────────────────
#  🎵 SMOOTH PROGRESS BAR
# ──────────────────────────────────────────────────────

def _bar(played, total):
    played_sec = time_to_seconds(played)
    total_sec = time_to_seconds(total) or 1
    pct = played_sec / total_sec

    filled = int(pct * 12)
    return "▬" * filled + "🔘" + "▬" * (12 - filled)


# ──────────────────────────────────────────────────────
#  🎧 STREAM UI (ULTIMATE)
# ──────────────────────────────────────────────────────

def stream_markup_timer(_, vidid, chat_id, played, dur, loop=False, shuffle=False, volume=100):

    bar = _bar(played, dur)

    return [

        # 🎵 PROGRESS LINE
        [
            InlineKeyboardButton(
                text=f"⌬ {_mono(played)}  {bar}  {_mono(dur)}",
                callback_data="progress"
            )
        ],

        # ⏩ SEEK CONTROL
        [
            InlineKeyboardButton("⏪ 10s", callback_data=f"ADMIN SeekBack|{chat_id}"),
            InlineKeyboardButton("⏩ 10s", callback_data=f"ADMIN SeekFwd|{chat_id}"),
        ],

        # 🎧 MAIN CONTROLS (CENTERED FEEL)
        [
            InlineKeyboardButton("⏮", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton("⏸", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN Skip|{chat_id}"),
        ],

        [
            InlineKeyboardButton("▶", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton("⏹", callback_data=f"ADMIN Stop|{chat_id}"),
        ],

        # 🎛️ EXTRA CONTROLS (SPOTIFY STYLE)
        [
            InlineKeyboardButton("🔁", callback_data=f"ADMIN ToggleLoop|{chat_id}"),
            InlineKeyboardButton("🔀", callback_data=f"ADMIN ToggleShuffle|{chat_id}"),
            InlineKeyboardButton(f"🔊 {_mono(str(volume))}%", callback_data=f"ADMIN Volume|{chat_id}"),
        ],

        # 🔊 VOLUME CONTROL
        [
            InlineKeyboardButton("🔉", callback_data=f"ADMIN VolDown|{chat_id}"),
            InlineKeyboardButton("🔊", callback_data=f"ADMIN VolUp|{chat_id}"),
        ],

        # ❌ CLOSE
        [
            InlineKeyboardButton("✖ Close", callback_data="close"),
        ],
    ]


# ──────────────────────────────────────────────────────
#  🎧 SIMPLE UI (NO TIMER)
# ──────────────────────────────────────────────────────

def stream_markup(_, videoid, chat_id):
    return [
        [
            InlineKeyboardButton("⏮", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton("⏸", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN Skip|{chat_id}"),
        ],
        [
            InlineKeyboardButton("▶", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton("⏹", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton("🔁", callback_data=f"ADMIN ToggleLoop|{chat_id}"),
            InlineKeyboardButton("🔀", callback_data=f"ADMIN ToggleShuffle|{chat_id}"),
        ],
        [
            InlineKeyboardButton("✖ Close", callback_data="close"),
        ],
    ]


# ──────────────────────────────────────────────────────
#  📋 QUEUE UI
# ──────────────────────────────────────────────────────

def queue_markup(_, chat_id, track_no: int, total: int):
    return [
        [
            InlineKeyboardButton(
                f"🎧 Queue {_mono(f'{track_no}/{total}')}",
                callback_data=f"ADMIN QueueInfo|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton("⏮", callback_data=f"ADMIN PrevTrack|{chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN NextTrack|{chat_id}"),
        ],
        [
            InlineKeyboardButton("🗑", callback_data=f"ADMIN ClearQueue|{chat_id}"),
            InlineKeyboardButton("✖", callback_data="close"),
        ],
    ]
