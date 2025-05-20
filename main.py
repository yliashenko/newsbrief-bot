import asyncio
from config import channel_groups
from digest_thread import DigestThread
from logger import logger
from cache import init_db
from telegram_client import start_client

async def main():
    await start_client()
    logger.info("🚀 Запуск асинхронної обробки потоків")

    tasks = []
    for category, channels in channel_groups.items():
        thread = DigestThread(category, channels)
        tasks.append(thread.run())

    await asyncio.gather(*tasks)
    logger.info("✅ Усі потоки оброблено")