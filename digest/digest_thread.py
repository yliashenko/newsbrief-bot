from typing import Any
from asyncio import Queue
from digest.fetcher import fetch_posts_for_channels 
from config import GROUP_EMOJIS, MIN_POST_LENGTH, MAX_POST_LENGTH
from shared.logger import logger


class DigestThread:
    def __init__(self, category: str, channels: list[str], llm_queue: Queue[dict[str, Any]]) -> None:
        self.category = category
        self.channels = channels
        self.emoji = GROUP_EMOJIS.get(category, "📝")
        self.llm_queue = llm_queue

    async def run(self) -> None:
        try:
            # 1. Отримання постів з каналів
            posts = await fetch_posts_for_channels(self.channels)
            logger.info(f"📦 Отримано {len(posts)} постів у потоці '{self.category}'")

            # Новий порядок фільтрації і логування
            too_short_posts = []
            too_long_posts = []
            final_posts = []

            # 2. Фільтрація постів за довжиною
            for post in posts:
                text = post.get("text", "").strip()
                channel = post["channel"]
                message_id = post["id"]
                length = len(text)

                if length < MIN_POST_LENGTH:
                    too_short_posts.append((channel, message_id, length))
                    continue

                if length > MAX_POST_LENGTH:
                    too_long_posts.append((channel, message_id, length))
                    continue

                final_posts.append(post)

            logger.info(f"🧾 '{self.category}': {len(final_posts)} нових, {len(posts) - len(final_posts)} відфільтровано")
            logger.info(f"✅ Нових постів для '{self.category}': {len(final_posts)}")
            logger.info(f"🧹 Всього відфільтровано {len(posts) - len(final_posts)} постів у '{self.category}'")

            for ch, msg_id, length in too_short_posts:
                logger.info(f"   ⛔ {ch}/{msg_id} — короткий ({length} симв.)")
            for ch, msg_id, length in too_long_posts:
                logger.info(f"   ⛔ {ch}/{msg_id} — занадто довгий ({length} симв.)")

            # 4. Передача всіх постів в LLM одним повідомленням
            if final_posts:
                await self.llm_queue.put({
                    "category": self.category,
                    "posts": final_posts,
                    "emoji": self.emoji
                })
            else:
                logger.info(f"📭 У потоці '{self.category}' немає нових постів для обробки")

            # 5. Обробка відповідей LLM відбувається в llm_worker
            # 6. Формування банера (опційно) — не реалізовано тут
            # 7. Надсилання повідомлення в Telegram — виконується в іншому модулі

        # Обробка помилок
        except Exception as e:
            logger.error(f"🔥 [{self.category}] Помилка у DigestThread: {e}")
