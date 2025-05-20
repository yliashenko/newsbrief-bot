import requests
from config import CHAT_ID, BOT_TOKEN
from logger import logger

def send_message(text: str, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": parse_mode
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        logger.debug("✅ Повідомлення успішно надіслано")
    else:
        logger.error(f"❌ Помилка при надсиланні повідомлення: {response.status_code} — {response.text}")