import asyncio
from config import channel_groups
from digest_thread import DigestThread
from telegram_client import start_client
from cache import init_db
from logger import logger

async def main():
    await start_client()
    logger.info("🚀 Starting asynchronous digest processing")

    tasks = []
    for category, channels in channel_groups.items():
        logger.debug(f"🧵 Preparing task for category: {category}")
        thread = DigestThread(category, channels)
        tasks.append(thread.run())

    await asyncio.gather(*tasks)
    logger.info("✅ All digest threads have been processed")

if __name__ == "__main__":
    try:
        logger.info("🐣 main.py launched")
        init_db()
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"❌ Uncaught exception during execution: {e}")