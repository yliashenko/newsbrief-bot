# pyright: reportAttributeAccessIssue=false
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramBadRequest
from config import STREAM_IMAGES
from .bot_instance import bot
from config import CHAT_ID, MAX_RETRIES, TELEGRAM_MESSAGE_LIMIT
from shared.logger import logger
from html import unescape
import asyncio
import re


def html_to_plain(html: str) -> str:
    text = re.sub(r'<a href="([^"]*)">[^<]*</a>', r"\1", html)
    text = re.sub(r"</?[bi]>", "", text)
    return unescape(text)[:TELEGRAM_MESSAGE_LIMIT]


async def send_plain_message(text: str) -> None:
    try:
        await bot.send_message(
            chat_id=str(CHAT_ID),
            text=text,
            parse_mode=None,
            disable_web_page_preview=True,
        )
        logger.info("✅ Дайджест надіслано простим текстом.")
    except Exception as e:
        logger.error(f"❌ Не вдалося надіслати навіть простий текст: {e}")


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
        except TelegramBadRequest as e:
            # Той самий текст Telegram відхилить знову, тому повтори не допоможуть
            logger.error(f"❌ Telegram відхилив HTML: {e}")
            await send_plain_message(html_to_plain(html))
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
    except Exception as e:
        # Банер необов'язковий: його збій не має блокувати текст дайджесту
        logger.warning(f"⚠️ Банер для '{category}' не надіслано: {e}")