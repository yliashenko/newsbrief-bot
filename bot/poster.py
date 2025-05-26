from aiogram.types import FSInputFile
from config import STREAM_IMAGES
from .bot_instance import bot
import requests
from config import CHAT_ID, BOT_TOKEN, MAX_RETRIES
from shared.logger import logger

from time import sleep
from loguru import logger

def send_html_message(html: str):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.debug(f"📤 HTML до Telegram:\n{html}")
            response = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": CHAT_ID,
                    "text": html,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
                timeout=15
            )
            resp_json = response.json()
            if response.status_code == 200 and resp_json.get("ok"):
                logger.info("✅ Повідомлення успішно надіслано в Telegram.")
                return
            else:
                raise Exception(f"{response.status_code} {response.reason}: {resp_json}")
        except Exception as e:
            logger.warning(f"⚠️ [Спроба {attempt}] Помилка надсилання повідомлення: {e}")
            if attempt < MAX_RETRIES:
                sleep(2 * attempt)
            else:
                logger.error("❌ Повідомлення не надіслано навіть після повторних спроб.")


# Async function to send a digest banner image for a category
async def send_digest_banner(category: str):
    image_path = STREAM_IMAGES.get(category)
    if not image_path:
        return

    image = FSInputFile(image_path)
    caption = f"Що нового в: {category.upper()}"
    await bot.send_photo(chat_id=CHAT_ID, photo=image, caption=caption)