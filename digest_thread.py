from fetcher import fetch_posts_for_channels
from formatter import format_digest
from poster import send_message
from config import GROUP_EMOJIS
from logger import logger

class DigestThread:
    def __init__(self, category: str, channels: list):
        self.category = category
        self.channels = channels
        self.emoji = GROUP_EMOJIS.get(category, "📝")

    async def run(self):
        logger.info(f"▶️ Старт потоку: {self.category}")
        posts = await fetch_posts_for_channels(self.channels)
        logger.info(f"📦 Отримано {len(posts)} постів у потоці '{self.category}'")

        digest = format_digest(self.category, posts, self.emoji)

        if digest:
            send_message(digest)
            logger.info(f"📬 Дайджест для '{self.category}' надіслано")
        else:
            logger.info(f"⏭️ Категорія '{self.category}' не відправлена (немає контенту або перевищено ліміт)")