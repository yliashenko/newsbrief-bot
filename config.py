import os
from dotenv import load_dotenv

load_dotenv()

# === Telegram + Groq API Keys ===
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# === LLM Settings ===
DEFAULT_MODEL = "mistral-saba-24b"
FALLBACK_MODEL = "mixtral-8x7b"
MAX_RETRIES = 3

# === Канали, згруповані по категоріях ===
channel_groups = {
    "ai": [
        "@denissexy",
        "@imatrofAI",
        "@seeallochnaya",
        "@ppprompt",
    ],
    "intresting": [
        "@spekamedia",
        "@iSIGHTmedia",
        "@wallstreetukr",
        "@MichaelPatsan",
        "@theworldisnoteasy",
        "@keddr",
    ],
    "crypto": [
        "@crypto_rostik",
    ],
    "politics": [
        "@OstanniyCapitalist",
        "@resurgammmm",
    ]
}

GROUP_EMOJIS = {
    "ai": "🤖",
    "intresting": "🔍",
    "crypto": "📈",
    "politics": "📑",
}