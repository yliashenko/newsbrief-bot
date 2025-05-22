import asyncio
from digest.digest_thread import DigestThread
from config import CHANNEL_GROUPS
from shared.logger import logger
from bot.formatter import format_digest
from bot.poster import send_html_message
from bot.telegram_client import client
from bot.cache import init_db
from chat_bot_ui.bot_handlers import router

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
dp.include_router(router)

llm_queue = asyncio.Queue()

async def run_digest_threads():
    for category, channels in CHANNEL_GROUPS.items():
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

import asyncio
from aiogram import asyncio as aiogram_asyncio

async def start_bot():
    await dp.start_polling(bot)

# запуск одночасно бота і дайджесту
async def main():
    logger.info("🚀 Starting asynchronous digest processing")
    await client.connect()

    # llm_worker
    worker_task = asyncio.create_task(llm_worker())

    # дайджести
    digest_task = asyncio.create_task(run_digest_threads())

    # стартуємо бота
    bot_task = asyncio.create_task(start_bot())

    await digest_task
    logger.info(f"🧪 Розмір черги після run_digest_threads: {llm_queue.qsize()}")
    await llm_queue.join()
    worker_task.cancel()
    bot_task.cancel()

if __name__ == "__main__":
    init_db()
    logger.info("🐣 main.py launched")
    asyncio.run(main())
