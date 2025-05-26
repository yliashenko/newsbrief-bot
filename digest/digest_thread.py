from digest.fetcher import fetch_posts_for_channels 
from config import GROUP_EMOJIS, MAX_POSTS_PER_REQUEST, MIN_POST_LENGTH
from shared.logger import logger
from bot.cache import PostCache  # 👈 додаємо

class DigestThread:
    def __init__(self, category: str, channels: list, llm_queue, post_cache: PostCache):
        self.category = category
        self.channels = channels
        self.emoji = GROUP_EMOJIS.get(category, "📝")
        self.llm_queue = llm_queue
        self.post_cache = post_cache

    from config import MIN_POST_LENGTH

    async def run(self):
        try:
            logger.info(f"▶️ Старт потоку: {self.category}")
            posts = await fetch_posts_for_channels(self.channels, self.post_cache)
            logger.info(f"📦 Отримано {len(posts)} постів у потоці '{self.category}'")

            filtered_posts = []
            skipped_posts = []  # 👈 масив для зібраних причин

            for post in posts:
                text = post.get("text", "").strip()
                channel = post["channel"]
                message_id = post["id"]

                if len(text) < MIN_POST_LENGTH:
                    skipped_posts.append({
                        "channel": channel,
                        "id": message_id,
                        "reason": "short",
                        "length": len(text)
                    })
                    continue

                if self.post_cache.is_cached(channel, message_id):
                    skipped_posts.append({
                        "channel": channel,
                        "id": message_id,
                        "reason": "cached"
                    })
                    continue

                filtered_posts.append(post)
                self.post_cache.add(channel, message_id)

            logger.info(f"✅ Нових постів для '{self.category}': {len(filtered_posts)}")
            logger.debug(f"🧹 Відфільтровано {len(skipped_posts)} постів у '{self.category}': {skipped_posts}")

            if len(filtered_posts) > MAX_POSTS_PER_REQUEST:
                logger.warning(f"✂️ Зрізано {len(filtered_posts) - MAX_POSTS_PER_REQUEST} постів через ліміт prompt")
                filtered_posts = filtered_posts[:MAX_POSTS_PER_REQUEST]

            if filtered_posts:
                await self.llm_queue.put({
                    "category": self.category,
                    "posts": filtered_posts,
                    "emoji": self.emoji
                })
            else:
                logger.info(f"📭 У потоці '{self.category}' немає нових постів для обробки")

        except Exception as e:
            logger.error(f"🔥 [{self.category}] Помилка у DigestThread: {e}")
