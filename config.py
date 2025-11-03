import os
from dotenv import load_dotenv
from pathlib import Path

# override=True гарантує що .env файл перезапише системні змінні
load_dotenv(override=True)

# === Telegram + Groq API Keys ===
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
# Очищаємо ключ від зайвих пробілів та символів нового рядка
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    GROQ_API_KEY = GROQ_API_KEY.strip()

# Діагностика: перевірка звідки завантажується ключ
import logging
_logger = logging.getLogger(__name__)
if GROQ_API_KEY:
    # Логуємо тільки початок та кінець для безпеки
    _logger.info(f"🔑 GROQ_API_KEY завантажено: {GROQ_API_KEY[:8]}...{GROQ_API_KEY[-8:]} (довжина: {len(GROQ_API_KEY)})")
    # Перевірка чи це правильний ключ
    if not GROQ_API_KEY.startswith("gsk_sJXF"):
        _logger.warning(f"⚠️  УВАГА: Завантажено ключ, який не відповідає очікуваному!")
        _logger.warning(f"   Очікується: gsk_sJXF...")
        _logger.warning(f"   Завантажено: {GROQ_API_KEY[:8]}...")
else:
    _logger.warning("GROQ_API_KEY не знайдено!")

# Перевірка що всі ключі встановлені
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY не встановлено в змінних середовища. Перевірте .env файл або Environment Variables на Render.")
if not GROQ_API_KEY.startswith("gsk_"):
    raise ValueError(f"❌ GROQ_API_KEY має некоректний формат (має починатися з 'gsk_'). Поточне значення: {GROQ_API_KEY[:10]}...")
if not API_ID or not API_HASH:
    raise ValueError("❌ API_ID або API_HASH не встановлено. Перевірте .env файл або Environment Variables на Render.")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не встановлено. Перевірте .env файл або Environment Variables на Render.")

# === Settings ===
# Оновлено: старі моделі більше не доступні на Groq API
# llama-3.3-70b-versatile - найближчий аналог до llama3-70b-8192 (70B параметрів)
DEFAULT_MODEL = "llama-3.3-70b-versatile"
# llama-3.1-8b-instant - швидша модель для fallback (замість mixtral-8x7b-32768)
FALLBACK_MODEL = "llama-3.1-8b-instant"
RATE_LIMIT_INTERVAL = 0.7  # seconds between LLM requests
MAX_RETRIES = 3
MAX_NEW_POSTS_PER_CHANNEL = 5
MAX_POSTS_PER_REQUEST = 10
MAX_POSTS_PER_CATEGORY = 20

MIN_POST_LENGTH = 100
MAX_POST_LENGTH = 4000

# Telegram message hard limit
TELEGRAM_MESSAGE_LIMIT = 4096

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

GROUP_EMOJIS = {
    "ai": "🤖",
    "media": "🔍",
    "blogs": "📑",
    "crypto": "📈",
    "politics": "📑",
}

POST_ENTRY_EMOJI = "📌"

CHANNEL_GROUPS = Path(__file__).parent / "channel_groups.json"

# === Stream banner images ===
STREAM_IMAGES = {
    "ai": "assets/banners/ai.jpg",
    "media": "assets/banners/media.jpg",
    "blogs": "assets/banners/blog.jpg",
    "crypto": "assets/banners/crypto.jpg",
    "politics": "assets/banners/politics.jpg",
}
