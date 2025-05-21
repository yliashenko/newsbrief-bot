from fetcher import fetch_posts_for_channels
from formatter import format_digest
from poster import send_message
from config import GROUP_EMOJIS, MAX_POSTS_PER_REQUEST
from logger import logger

  # обмеження для уникнення 413

class DigestThread:
    def __init__(self, category: str, channels: list):
        self.category = category
        self.channels = channels
        self.emoji = GROUP_EMOJIS.get(category, "📝")

    async def run(self):
        logger.info(f"▶️ Старт потоку: {self.category}")
        posts = await fetch_posts_for_channels(self.channels)
        logger.info(f"📦 Отримано {len(posts)} постів у потоці '{self.category}'")

        # обрізаємо, якщо постів більше ніж дозволено
        if len(posts) > MAX_POSTS_PER_REQUEST:
            logger.warning(f"✂️ Зрізано {len(posts) - MAX_POSTS_PER_REQUEST} постів через ліміт prompt")
            posts = posts[:MAX_POSTS_PER_REQUEST]

        digest = await format_digest(self.category, posts, self.emoji)

        if digest:
            send_message(digest)
            logger.info(f"📬 Дайджест для '{self.category}' надіслано")
        else:
            logger.info(f"⏭️ Категорія '{self.category}' не відправлена (немає контенту або перевищено ліміт)")