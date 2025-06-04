# pyright: reportAttributeAccessIssue=false
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramBadRequest
from config import STREAM_IMAGES
from .bot_instance import bot
from config import CHAT_ID, MAX_RETRIES
from shared.logger import logger
import asyncio

async def send_html_message(html: str) -> None:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.debug(f"📤 HTML до Telegram:\n{html}")
            await bot.send_message(
                chat_id=str(CHAT_ID),
                text=html,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            logger.info("✅ Повідомлення успішно надіслано в Telegram.")
            return
        except Exception as e:
            logger.warning(f"⚠️ [Спроба {attempt}] Помилка надсилання повідомлення: {e}")
            if attempt < MAX_RETRIES:
                await asyncio.sleep(2 * attempt)
            else:
                logger.error("❌ Повідомлення не надіслано навіть після повторних спроб.")


# Async function to send a digest banner image for a category
async def send_digest_banner(category: str) -> None:
    image_path = STREAM_IMAGES.get(category)
    if not image_path:
        logger.warning(f"🚫 Немає банера для категорії '{category}'")
        return

    image = FSInputFile(image_path)
    try:
        await bot.send_photo(chat_id=str(CHAT_ID), photo=image)
        logger.info(f"✅ Банер для '{category}' надіслано")
    except TelegramBadRequest as e:
        if "PHOTO_INVALID_DIMENSIONS" in str(e):
            logger.warning(f"⚠️ Банер для '{category}' не надіслано: невірні розміри зображення")
        else:
            logger.error(f"❌ Помилка надсилання банера для '{category}': {e}")