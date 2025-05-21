import requests
from config import CHAT_ID, BOT_TOKEN, MAX_RETRIES
from shared.logger import logger

from time import sleep
from loguru import logger

def send_html_message(html: str):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
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
            if response.status_code == 200:
                logger.info("✅ Повідомлення успішно надіслано в Telegram.")
                return
            else:
                raise Exception(f"{response.status_code} {response.reason}: {response.text}")
        except Exception as e:
            logger.warning(f"⚠️ [Спроба {attempt}] Помилка надсилання повідомлення: {e}")
            if attempt < MAX_RETRIES:
                sleep(2 * attempt)
            else:
                logger.error("❌ Повідомлення не надіслано навіть після повторних спроб.")