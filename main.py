import asyncio
from config import channel_groups
from digest_thread import DigestThread
from telegram_client import start_client
from cache import init_db
from logger import logger

MAX_PARALLEL_THREADS = 2
semaphore = asyncio.Semaphore(MAX_PARALLEL_THREADS)

async def run_thread_with_limit(thread: DigestThread):
    async with semaphore:
        await thread.run()

async def main():
    await start_client()
    logger.info("🚀 Starting asynchronous digest processing")

    tasks = []
    for category, channels in channel_groups.items():
        logger.debug(f"🧵 Preparing task for category: {category}")
        thread = DigestThread(category, channels)
        tasks.append(run_thread_with_limit(thread))

    await asyncio.gather(*tasks)
    logger.info("✅ All digest threads have been processed")

if __name__ == "__main__":
    try:
        logger.info("🐣 main.py launched")
        init_db()
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"❌ Uncaught exception during execution: {e}")