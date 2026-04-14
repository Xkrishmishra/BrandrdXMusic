import math
from pyrogram.types import InlineKeyboardButton
from BrandrdXMusic.utils.formatters import time_to_seconds


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              PROGRESS BAR ENGINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_BAR_FILLED = "█"
_BAR_HALF   = "▓"
_BAR_EMPTY  = "░"
_BAR_LEN    = 10

def _build_bar(percentage: float) -> str:
    """Smooth 10-slot progress bar with half-step indicator."""
    filled = int(percentage / 10)
    half   = 1 if (percentage % 10) >= 5 else 0
    empty  = _BAR_LEN - filled - half
    return _BAR_FILLED * filled + _BAR_HALF * half + _BAR_EMPTY * empty


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              TRACK MARKUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def track_markup(_, videoid, user_id, channel, fplay):
    """Choose stream mode: Audio-only or Video."""
    return [
        [
            InlineKeyboardButton(
                text=f"♫  {_['P_B_1']}",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=f"◈  {_['P_B_2']}",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"✕  {_['CLOSE_BUTTON']}",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#         STREAM MARKUP  ·  WITH TIMER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def stream_markup_timer(_, vidid, chat_id, played, dur):
    """Live playback panel with smooth progress bar."""
    played_sec    = time_to_seconds(played)
    duration_sec  = time_to_seconds(dur) or 1
    percentage    = min((played_sec / duration_sec) * 100, 100)
    bar           = _build_bar(percentage)
    pct_label     = f"{math.floor(percentage)}%"

    return [
        # ── Progress Row ──────────────────────────────
        [
            InlineKeyboardButton(
                text=f"◷  {played}  {bar}  {dur}  ·  {pct_label}",
                callback_data="GetTimer",
            )
        ],
        # ── Primary Controls ──────────────────────────
        [
            InlineKeyboardButton(text="⏮  Replay",  callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="⏸  Pause",   callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="⏭  Skip",    callback_data=f"ADMIN Skip|{chat_id}"),
        ],
        # ── Secondary Controls ────────────────────────
        [
            InlineKeyboardButton(text="▶  Resume",  callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="⏹  Stop",    callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        # ── Dismiss ───────────────────────────────────
        [
            InlineKeyboardButton(text=f"✕  {_['CLOSE_BUTTON']}", callback_data="close"),
        ],
    ]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#         STREAM MARKUP  ·  NO TIMER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def stream_markup(_, videoid, chat_id):
    """Compact playback panel without progress bar."""
    return [
        [
            InlineKeyboardButton(text="⏮  Replay",  callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="⏸  Pause",   callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="⏭  Skip",    callback_data=f"ADMIN Skip|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="▶  Resume",  callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="⏹  Stop",    callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text=f"✕  {_['CLOSE_BUTTON']}", callback_data="close"),
        ],
    ]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              PLAYLIST MARKUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=f"♫  {_['P_B_1']}",
                callback_data=f"Playlists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=f"◈  {_['P_B_2']}",
                callback_data=f"Playlists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"✕  {_['CLOSE_BUTTON']}",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#             LIVESTREAM MARKUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=f"⦿  {_['P_B_3']}  ·  LIVE",
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"✕  {_['CLOSE_BUTTON']}",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              SLIDER MARKUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    short_query = query[:20]
    return [
        [
            InlineKeyboardButton(
                text=f"♫  {_['P_B_1']}",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=f"◈  {_['P_B_2']}",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀  Prev",
                callback_data=f"slider B|{query_type}|{short_query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=f"✕  {_['CLOSE_BUTTON']}",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="Next  ▶",
                callback_data=f"slider F|{query_type}|{short_query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
