from bot.telegram_client import get_channel_posts
from shared.logger import logger
from typing import List, Any

async def fetch_posts_for_channels(channels: List[str], limit: int = 20) -> List[Any]:
    all_posts = []

    for channel in channels:
        try:
            posts = await get_channel_posts(channel, limit)

            if not posts:
                logger.warning(f"⚠️ Порожній результат або None з @{channel}")
                continue

            all_posts.extend(posts)
            logger.info(f"📨 {channel} → {len(posts)} постів")

        except Exception as e:
            logger.warning(f"⚠️ Не вдалося отримати пости з {channel}: {e}")

    return all_posts