import os
from dotenv import load_dotenv

load_dotenv()

# === Telegram + Groq API Keys ===
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# === Settings ===
DEFAULT_MODEL = "mistral-saba-24b"
FALLBACK_MODEL = "llama3-8b-8192"
MAX_RETRIES = 3
MAX_NEW_POSTS_PER_CHANNEL = 15

MAX_PARALLEL_THREADS = 2
MAX_CONCURRENT_THREADS = 2
MAX_POSTS_PER_REQUEST = 10

SYSTEM_PROMPT = (
    "Ти — бот, що формує щоденні дайджести з Telegram-постів українською мовою. "
    "Твоє завдання — стиснути пост, зберігаючи ключову суть і настрій, у формат:\n"
    "- <Заголовок> (1 речення)\n"
    "- <Короткий опис> (1–2 речення)\n\n"
    "ВАЖЛИВІ МОМЕНТИ:\n"
    "🔒 Не додавай додаткових вступів.\n"
    "🔒 Не додавай додаткових нумерацій.\n"
    "🔒 Не додавай типів постів, категорії або підзаголовки.\n"
    "🔒 Не додавай жодних заголовків, пояснень або коментарів не повʼязаних із змістом постів.\n"
    "🔒 Відповідай виключно українською мовою незалежно від мови постів.\n"
)

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
        "@prostirspokoy",
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

POST_ENTRY_EMOJI = "📌"