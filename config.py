import re
import os
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# --- STARK INDUSTRIES: CORE CONFIG ---
API_ID = int(getenv("API_ID", "0")) 
API_HASH = getenv("API_HASH", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)

# --- DATABASE ---
MONGO_DB_URI = getenv("MONGO_DB_URI", None)
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", "Avengers Music")
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", None)

# --- OWNER CONTROL (NO HARDCODED ID) ---
# Maine purani hacker ID (7250012103) hata di hai. 
# Ab bot wahi ID lega jo aap Heroku/VPS mein OWNER_ID variable mein dalenge.
OWNER_ID = int(getenv("OWNER_ID", "7458057585")) 

# --- LOGGING & LIMITS ---
LOGGER_ID = int(getenv("LOGGER_ID", None))
LOG = bool(getenv("LOG", True))
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 900))


# --- DEPLOYMENT TOOLS ---
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/xkrishmishra/krish_music")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)

# --- SUPPORT LINKS ---
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/krishnetwork")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/krishsupport")

# --- ASSISTANT PROTOCOLS ---
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# SECURITY FIX: Auto Gcast ko False rakha hai hacker ke spam se bachne ke liye.
AUTO_GCAST = False
AUTO_GCAST_MSG = getenv("AUTO_GCAST_MSG", "")

# --- SPOTIFY ---
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "bcfe26b0ebc3428882a0b5fb3e872473")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "907c6a054c214005aeae1fd752273cc4")


# --- LIMITS & DOWNLOADS ---
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "50"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "180"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "2000"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))

# --- SESSIONS ---
STRING1 = getenv("STRING_SESSION",  None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# --- INTERNALS ---
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# --- MCU THEME: IMAGE ASSETS ---
START_IMG_URL = getenv("START_IMG_URL", "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg")
PLAYLIST_IMG_URL = "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg"
STATS_IMG_URL = "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg"
STREAM_IMG_URL = "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/01c9f81cea701069de02d-9f2812d4759c53e5d4.jpg"

# --- UTILS ---
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# --- URL VALIDATION ---
if SUPPORT_CHANNEL and not re.match("(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHANNEL URL.")

if SUPPORT_CHAT and not re.match("(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHAT URL.")
    
