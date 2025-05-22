from digest.fetcher import fetch_posts_for_channels
from config import GROUP_EMOJIS, MAX_POSTS_PER_REQUEST
from shared.logger import logger

class DigestThread:
    def __init__(self, category: str, channels: list, llm_queue):
        self.category = category
        self.channels = channels
        self.emoji = GROUP_EMOJIS.get(category, "📝")
        self.llm_queue = llm_queue

    async def run(self):
        try:
            logger.info(f"▶️ Старт потоку: {self.category}")
            posts = await fetch_posts_for_channels(self.channels)
            logger.info(f"📦 Отримано {len(posts)} постів у потоці '{self.category}'")

            if len(posts) > MAX_POSTS_PER_REQUEST:
                logger.warning(f"✂️ Зрізано {len(posts) - MAX_POSTS_PER_REQUEST} постів через ліміт prompt")
                posts = posts[:MAX_POSTS_PER_REQUEST]

            for post in posts:
                await self.llm_queue.put({
                    "category": self.category,
                    "post": post,
                    "emoji": self.emoji
                })
        except Exception as e:
            logger.error(f"🔥 [{self.category}] Помилка у DigestThread: {e}")