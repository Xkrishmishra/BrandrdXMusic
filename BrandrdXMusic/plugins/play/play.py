"""
╔══════════════════════════════════════════════╗
║        🎵  BrandrdXMusic — Play Module       ║
║   Handles /play, /vplay, /cplay + callbacks  ║
╚══════════════════════════════════════════════╝
"""

import random
import string

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from BrandrdXMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.utils import seconds_to_min, time_to_seconds
from BrandrdXMusic.utils.channelplay import get_channeplayCB
from BrandrdXMusic.utils.decorators.language import languageCB
from BrandrdXMusic.utils.decorators.play import PlayWrapper
from BrandrdXMusic.utils.formatters import formats
from BrandrdXMusic.utils.inline import (
    botplaylist_markup,
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from BrandrdXMusic.utils.logger import play_logs
from BrandrdXMusic.utils.stream.stream import stream
from config import BANNED_USERS, lyrical


# ─────────────────────────────────────────────
#  🔧  Shared Helpers
# ─────────────────────────────────────────────

async def _err(mystic, ex, _):
    """Edit mystic message with a clean error; returns None so callers can `return await _err(...)`."""
    ex_type = type(ex).__name__
    msg = ex if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
    return await mystic.edit_text(msg)


async def _stream_or_err(mystic, _, *args, **kwargs):
    """Call stream(); on failure edit mystic and return False, else return True."""
    try:
        await stream(_, mystic, *args, **kwargs)
        return True
    except Exception as e:
        await _err(mystic, e, _)
        return False


def _rand_hash(k=10):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=k))


# ─────────────────────────────────────────────
#  ▶  /play  /vplay  /cplay  /cvplay  (+ force)
# ─────────────────────────────────────────────

@app.on_message(
    filters.command([
        "play", "vplay", "cplay", "cvplay",
        "playforce", "vplayforce", "cplayforce", "cvplayforce",
    ])
    & filters.group
    & ~BANNED_USERS
)
@PlayWrapper
async def play_commnd(client, message: Message, _, chat_id, video, channel, playmode, url, fplay):
    mystic = await message.reply_text(_["play_2"].format(channel) if channel else _["play_1"])

    # ── Init state ──────────────────────────────────────────
    plist_id = plist_type = spotify = None
    slider = False
    user_id   = message.from_user.id
    user_name = message.from_user.first_name

    reply = message.reply_to_message
    audio_tg = (reply.audio or reply.voice)     if reply else None
    video_tg = (reply.video or reply.document)  if reply else None

    # ── 1. Telegram audio reply ──────────────────────────────
    if audio_tg:
        if audio_tg.file_size > 104_857_600:
            return await mystic.edit_text(_["play_5"])
        if audio_tg.duration > config.DURATION_LIMIT:
            return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, app.mention))

        path = await Telegram.get_filepath(audio=audio_tg)
        if not await Telegram.download(_, message, mystic, path):
            return

        details = {
            "title": await Telegram.get_filename(audio_tg, audio=True),
            "link":  await Telegram.get_link(message),
            "path":  path,
            "dur":   await Telegram.get_duration(audio_tg, path),
        }
        ok = await _stream_or_err(mystic, _, user_id, details, chat_id, user_name,
                                   message.chat.id, streamtype="telegram", forceplay=fplay)
        return await mystic.delete() if ok else None

    # ── 2. Telegram video / document reply ──────────────────
    elif video_tg:
        if reply.document:
            ext = getattr(video_tg, "file_name", "").split(".")[-1].lower()
            if ext not in formats:
                return await mystic.edit_text(_["play_7"].format(" | ".join(formats)))
        if video_tg.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_8"])

        path = await Telegram.get_filepath(video=video_tg)
        if not await Telegram.download(_, message, mystic, path):
            return

        details = {
            "title": await Telegram.get_filename(video_tg),
            "link":  await Telegram.get_link(message),
            "path":  path,
            "dur":   await Telegram.get_duration(video_tg, path),
        }
        ok = await _stream_or_err(mystic, _, user_id, details, chat_id, user_name,
                                   message.chat.id, video=True, streamtype="telegram", forceplay=fplay)
        return await mystic.delete() if ok else None

    # ── 3. URL branch ────────────────────────────────────────
    elif url:
        # ── YouTube ──
        if await YouTube.exists(url):
            if "playlist" in url:
                try:
                    details = await YouTube.playlist(url, config.PLAYLIST_FETCH_LIMIT, user_id)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "yt"
                plist_id   = (url.split("=")[1]).split("&")[0] if "&" in url else url.split("=")[1]
                img, cap   = config.PLAYLIST_IMG_URL, _["play_9"]
            else:
                try:
                    details, track_id = await YouTube.track(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_10"].format(details["title"], details["duration_min"])

        # ── Spotify ──
        elif await Spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text("» sᴘᴏᴛɪғʏ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ ʏᴇᴛ.\n\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")

            _sp_map = {
                "track":    (Spotify.track,   "youtube",  config.SPOTIFY_PLAYLIST_IMG_URL, None),
                "playlist": (Spotify.playlist, "playlist", config.SPOTIFY_PLAYLIST_IMG_URL, "spplay"),
                "album":    (Spotify.album,    "playlist", config.SPOTIFY_ALBUM_IMG_URL,    "spalbum"),
                "artist":   (Spotify.artist,   "playlist", config.SPOTIFY_ARTIST_IMG_URL,   "spartist"),
            }
            matched = next((k for k in _sp_map if k in url), None)
            if not matched:
                return await mystic.edit_text(_["play_15"])

            fn, streamtype, sp_img, sp_ptype = _sp_map[matched]
            try:
                result = await fn(url)
            except Exception:
                return await mystic.edit_text(_["play_3"])

            if matched == "track":
                details, track_id = result
                img = details["thumb"]
                cap = _["play_10"].format(details["title"], details["duration_min"])
            else:
                details, plist_id = result
                plist_type = sp_ptype
                img = sp_img
                cap = _["play_11"].format(
                    message.from_user.first_name if matched == "artist"
                    else app.mention, message.from_user.mention
                )

        # ── Apple Music ──
        elif await Apple.valid(url):
            if "album" in url:
                try:
                    details, track_id = await Apple.track(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_10"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                spotify = True
                try:
                    details, plist_id = await Apple.playlist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "apple"
                cap = _["play_12"].format(app.mention, message.from_user.mention)
                img = url
            else:
                return await mystic.edit_text(_["play_3"])

        # ── Resso ──
        elif await Resso.valid(url):
            try:
                details, track_id = await Resso.track(url)
            except Exception:
                return await mystic.edit_text(_["play_3"])
            streamtype = "youtube"
            img = details["thumb"]
            cap = _["play_10"].format(details["title"], details["duration_min"])

        # ── SoundCloud ──
        elif await SoundCloud.valid(url):
            try:
                details, track_path = await SoundCloud.download(url)
            except Exception:
                return await mystic.edit_text(_["play_3"])
            if details["duration_sec"] > config.DURATION_LIMIT:
                return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, app.mention))
            ok = await _stream_or_err(mystic, _, user_id, details, chat_id, user_name,
                                       message.chat.id, streamtype="soundcloud", forceplay=fplay)
            return await mystic.delete() if ok else None

        # ── Raw / Index / M3U8 ──
        else:
            try:
                await Hotty.stream_call(url)
            except NoActiveGroupCall:
                await mystic.edit_text(_["black_9"])
                return await app.send_message(chat_id=config.LOGGER_ID, text=_["play_17"])
            except Exception as e:
                return await mystic.edit_text(_["general_2"].format(type(e).__name__))

            await mystic.edit_text(_["str_2"])
            ok = await _stream_or_err(mystic, _, message.from_user.id, url, chat_id,
                                       message.from_user.first_name, message.chat.id,
                                       video=video, streamtype="index", forceplay=fplay)
            return await play_logs(message, streamtype="M3u8 or Index Link") if ok else None

    # ── 4. Text search (no URL) ──────────────────────────────
    else:
        if len(message.command) < 2:
            return await mystic.edit_text(
                _["play_18"],
                reply_markup=InlineKeyboardMarkup(botplaylist_markup(_)),
            )
        slider = True
        query  = message.text.split(None, 1)[1].replace("-v", "").strip()
        try:
            details, track_id = await YouTube.track(query)
        except Exception:
            return await mystic.edit_text(_["play_3"])
        streamtype = "youtube"

    # ── 5. Direct-play mode ──────────────────────────────────
    if str(playmode) == "Direct":
        if not plist_type:
            if details.get("duration_min"):
                if time_to_seconds(details["duration_min"]) > config.DURATION_LIMIT:
                    return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, app.mention))
            else:
                buttons = livestream_markup(_, track_id, user_id,
                                            "v" if video else "a",
                                            "c" if channel else "g",
                                            "f" if fplay else "d")
                return await mystic.edit_text(_["play_13"], reply_markup=InlineKeyboardMarkup(buttons))

        ok = await _stream_or_err(mystic, _, user_id, details, chat_id, user_name,
                                   message.chat.id, video=video, streamtype=streamtype,
                                   spotify=spotify, forceplay=fplay)
        if ok:
            await mystic.delete()
            return await play_logs(message, streamtype=streamtype)

    # ── 6. Inline / slider mode ──────────────────────────────
    else:
        await mystic.delete()
        if plist_type:
            ran_hash = _rand_hash()
            lyrical[ran_hash] = plist_id
            buttons = playlist_markup(_, ran_hash, user_id, plist_type,
                                      "c" if channel else "g", "f" if fplay else "d")
            await message.reply_photo(photo=img, caption=cap,
                                      reply_markup=InlineKeyboardMarkup(buttons))
            return await play_logs(message, streamtype=f"Playlist : {plist_type}")

        elif slider:
            buttons = slider_markup(_, track_id, user_id, query, 0,
                                    "c" if channel else "g", "f" if fplay else "d")
            await message.reply_photo(
                photo=details["thumb"],
                caption=_["play_10"].format(details["title"].title(), details["duration_min"]),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return await play_logs(message, streamtype="Searched on Youtube")

        else:
            buttons = track_markup(_, track_id, user_id,
                                   "c" if channel else "g", "f" if fplay else "d")
            await message.reply_photo(photo=img, caption=cap,
                                      reply_markup=InlineKeyboardMarkup(buttons))
            return await play_logs(message, streamtype="URL Searched Inline")


# ─────────────────────────────────────────────
#  🎛  Callback — MusicStream
# ─────────────────────────────────────────────

@app.on_callback_query(filters.regex("MusicStream") & ~BANNED_USERS)
@languageCB
async def play_music(client, CallbackQuery, _):
    cb = CallbackQuery.data.strip().split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = cb.split("|")

    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except Exception:
            return

    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except Exception:
        return

    user_name = CallbackQuery.from_user.first_name
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except Exception:
        pass

    mystic = await CallbackQuery.message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )

    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception:
        return await mystic.edit_text(_["play_3"])

    if details["duration_min"]:
        if time_to_seconds(details["duration_min"]) > config.DURATION_LIMIT:
            return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, app.mention))
    else:
        buttons = livestream_markup(_, track_id, CallbackQuery.from_user.id, mode,
                                    "c" if cplay == "c" else "g", "f" if fplay else "d")
        return await mystic.edit_text(_["play_13"], reply_markup=InlineKeyboardMarkup(buttons))

    ok = await _stream_or_err(
        mystic, _,
        CallbackQuery.from_user.id, details, chat_id, user_name,
        CallbackQuery.message.chat.id,
        True if mode == "v" else None,
        streamtype="youtube",
        forceplay=(True if fplay == "f" else None),
    )
    return await mystic.delete() if ok else None


# ─────────────────────────────────────────────
#  👤  Callback — AnonymousAdmin
# ─────────────────────────────────────────────

@app.on_callback_query(filters.regex("AnonymousAdmin") & ~BANNED_USERS)
async def piyush_check(client, CallbackQuery):
    try:
        await CallbackQuery.answer(
            "» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ :\n\n"
            "ᴏᴘᴇɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ sᴇᴛᴛɪɴɢs.\n"
            "-> ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀs\n-> ᴄʟɪᴄᴋ ᴏɴ ʏᴏᴜʀ ɴᴀᴍᴇ\n"
            "-> ᴜɴᴄʜᴇᴄᴋ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs.",
            show_alert=True,
        )
    except Exception:
        pass


# ─────────────────────────────────────────────
#  📋  Callback — HottyPlaylists
# ─────────────────────────────────────────────

@app.on_callback_query(filters.regex("HottyPlaylists") & ~BANNED_USERS)
@languageCB
async def play_playlists_command(client, CallbackQuery, _):
    cb = CallbackQuery.data.strip().split(None, 1)[1]
    videoid, user_id, ptype, mode, cplay, fplay = cb.split("|")

    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except Exception:
            return

    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except Exception:
        return

    user_name = CallbackQuery.from_user.first_name
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except Exception:
        pass

    mystic  = await CallbackQuery.message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )
    videoid = lyrical.get(videoid)
    video   = True if mode == "v" else None
    ffplay  = True if fplay == "f" else None
    spotify = ptype != "yt"

    _fetch = {
        "yt":      lambda: YouTube.playlist(videoid, config.PLAYLIST_FETCH_LIMIT,
                                             CallbackQuery.from_user.id, True),
        "spplay":  lambda: Spotify.playlist(videoid),
        "spalbum": lambda: Spotify.album(videoid),
        "spartist":lambda: Spotify.artist(videoid),
        "apple":   lambda: Apple.playlist(videoid, True),
    }
    try:
        result = await _fetch[ptype]()
        # yt returns a plain list; others return (result, id)
        if ptype != "yt":
            result, _ = result
    except Exception:
        return await mystic.edit_text(_["play_3"])

    ok = await _stream_or_err(
        mystic, _,
        user_id, result, chat_id, user_name,
        CallbackQuery.message.chat.id,
        video,
        streamtype="playlist",
        spotify=spotify,
        forceplay=ffplay,
    )
    return await mystic.delete() if ok else None


# ─────────────────────────────────────────────
#  🎞  Callback — Slider (← →)
# ─────────────────────────────────────────────

@app.on_callback_query(filters.regex("slider") & ~BANNED_USERS)
@languageCB
async def slider_queries(client, CallbackQuery, _):
    cb = CallbackQuery.data.strip().split(None, 1)[1]
    what, rtype, query, user_id, cplay, fplay = cb.split("|")
    rtype = int(rtype)

    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except Exception:
            return

    # Forward → wraps 9→0; Backward ← wraps 0→9
    if what == "F":
        query_type = 0 if rtype == 9 else rtype + 1
    else:
        query_type = 9 if rtype == 0 else rtype - 1

    try:
        await CallbackQuery.answer(_["playcb_2"])
    except Exception:
        pass

    title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)
    buttons = slider_markup(_, vidid, user_id, query, query_type, cplay, fplay)
    med = InputMediaPhoto(
        media=thumbnail,
        caption=_["play_10"].format(title.title(), duration_min),
    )
    return await CallbackQuery.edit_message_media(
        media=med, reply_markup=InlineKeyboardMarkup(buttons)
    )
