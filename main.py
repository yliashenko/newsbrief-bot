import asyncio
from digest.digest_thread import DigestThread
import json
from config import CHANNEL_GROUPS as CHANNEL_GROUPS_PATH
from shared.logger import logger
from bot.formatter import format_digest
from bot.poster import send_html_message
from bot.telegram_client import client
from bot.cache import init_db

llm_queue = asyncio.Queue()

async def run_digest_threads():
    with open(CHANNEL_GROUPS_PATH, "r", encoding="utf-8") as f:
        groups = json.load(f)

    for category, channels in groups.items():
        thread = DigestThread(category, channels, llm_queue)
        await thread.run()

async def llm_worker():
    while True:
        try:
            task = await llm_queue.get()
            category = task["category"]
            posts = task["posts"]
            emoji = task["emoji"]
            logger.info(f"🎯 llm_worker отримав задачу: {category} ({len(posts)} постів)")

            digest = await format_digest(category, posts, emoji)

            if digest:
                send_html_message(digest)
                logger.info(f"📬 Дайджест для '{category}' надіслано")
            else:
                logger.info(f"⏭️ Категорія '{category}' не відправлена (немає контенту або перевищено ліміт)")

            llm_queue.task_done()
        except Exception as e:
            logger.exception(f"💥 Помилка в llm_worker: {e}")

async def main():
    logger.info("🚀 Starting asynchronous digest processing")
    await client.connect()

    worker_task = asyncio.create_task(llm_worker())
    digest_task = asyncio.create_task(run_digest_threads())

    await digest_task
    logger.info(f"🧪 Розмір черги після run_digest_threads: {llm_queue.qsize()}")
    await llm_queue.join()
    worker_task.cancel()

if __name__ == "__main__":
    init_db()
    logger.info("🐣 main.py launched")
    asyncio.run(main())
