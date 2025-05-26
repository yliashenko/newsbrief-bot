from bot.telegram_client import get_channel_posts
from shared.logger import logger
from config import MAX_NEW_POSTS_PER_CHANNEL
from bot.cache import PostCache  # ✅ новий клас кешу

async def fetch_posts_for_channels(channels: list, post_cache: PostCache, limit: int = 20) -> list:
    all_posts = []

    for channel in channels:
        try:
            posts = await get_channel_posts(channel, limit)

            if not posts:
                logger.warning(f"⚠️ Порожній результат або None з @{channel}")
                continue

            new_posts = []
            for post in posts:
                message_id = post.get("id")
                if not post_cache.is_cached(channel, message_id):
                    new_posts.append(post)
                    post_cache.add(channel, message_id)
                else:
                    logger.debug(f"🔁 {channel} — вже бачили post #{message_id}")

            new_posts = new_posts[:MAX_NEW_POSTS_PER_CHANNEL]
            logger.info(f"📨 {channel} → {len(new_posts)} нових постів (з {len(posts)})")
            all_posts.extend(new_posts)

        except Exception as e:
            logger.warning(f"⚠️ Не вдалося отримати пости з {channel}: {e}")

    return all_posts