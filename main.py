import asyncio
from digest.digest_thread import DigestThread
from config import channel_groups, MAX_CONCURRENT_THREADS
from shared.logger import logger
from bot.formatter import format_digest
from bot.poster import send_message
from bot.telegram_client import client

llm_queue = asyncio.Queue()
semaphore = asyncio.Semaphore(MAX_CONCURRENT_THREADS)

async def run_digest_threads():
    tasks = []
    for category, channels in channel_groups.items():
        thread = DigestThread(category, channels, llm_queue)
        tasks.append(run_thread_with_limit(thread))
    await asyncio.gather(*tasks)

async def run_thread_with_limit(thread):
    async with semaphore:
        await thread.run()

async def llm_worker():
    while True:
        task = await llm_queue.get()
        category = task["category"]
        posts = task["posts"]
        emoji = task["emoji"]

        digest = await format_digest(category, posts, emoji)

        if digest:
            send_message(digest)
            logger.info(f"📬 Дайджест для '{category}' надіслано")
        else:
            logger.info(f"⏭️ Категорія '{category}' не відправлена (немає контенту або перевищено ліміт)")

        llm_queue.task_done()

async def main():
    logger.info("🚀 Starting asynchronous digest processing")
    await client.connect()
    worker_task = asyncio.create_task(llm_worker())
    await run_digest_threads()
    await llm_queue.join()
    worker_task.cancel()

if __name__ == "__main__":
    logger.info("🐣 main.py launched")
    asyncio.run(main())
