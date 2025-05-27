from typing import Any, TYPE_CHECKING
import asyncio
import json
from config import CHANNEL_GROUPS
from shared.logger import logger
from bot.formatter import format_digest
from bot.poster import send_html_message
from bot.poster import send_digest_banner
from bot.telegram_client import client
from bot.cache import init_db, PostCache
from digest.digest_thread import DigestThread

llm_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
post_cache = PostCache()

async def run_digest_threads() -> None:
    with open(CHANNEL_GROUPS, "r", encoding="utf-8") as f:
        groups = json.load(f)

    for category, channels in groups.items():
        thread = DigestThread(category, channels, llm_queue, post_cache)
        await thread.run()

async def llm_worker() -> None:
    while True:
        try:
            task = await llm_queue.get()
            category = task["category"]
            posts = task["posts"]
            emoji = task["emoji"]
            logger.info(f"🎯 llm_worker отримав задачу: {category} ({len(posts)} постів)")

            digest = await format_digest(category, posts, emoji)

            if digest:
                await send_digest_banner(category)
                send_html_message(digest)
                logger.info(f"📬 Дайджест для '{category}' надіслано")
            else:
                logger.info(f"⏭️ Категорія '{category}' не відправлена (немає контенту або перевищено ліміт)")

            llm_queue.task_done()
        except Exception as e:
            logger.exception(f"💥 Помилка в llm_worker: {e}")

async def main() -> None:
    await client.connect()

    worker_task = asyncio.create_task(llm_worker())
    digest_task = asyncio.create_task(run_digest_threads())

    await digest_task
    await llm_queue.join()
    worker_task.cancel()

    post_cache.save()

if __name__ == "__main__":
    init_db()
    asyncio.run(main())
