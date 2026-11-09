from typing import Any, TYPE_CHECKING
import asyncio
import json
from config import CHANNEL_GROUPS
from shared.logger import logger
from bot.formatter import format_digest
from bot.poster import send_html_message
from bot.poster import send_digest_banner
from bot.telegram_client import client, close_client, start_client
from bot.bot_instance import bot
from digest.digest_thread import DigestThread

llm_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

async def run_digest_threads() -> None:
    with open(CHANNEL_GROUPS, "r", encoding="utf-8") as f:
        groups = json.load(f)

    for category, channels in groups.items():
        thread = DigestThread(category, channels, llm_queue)
        await thread.run()

async def llm_worker() -> None:
    while True:
        task = await llm_queue.get()
        try:
            category = task["category"]
            posts = task["posts"]
            emoji = task["emoji"]
            logger.info(f"🎯 llm_worker отримав задачу: {category} ({len(posts)} постів)")

            digest = await format_digest(category, posts, emoji)

            if digest:
                await send_digest_banner(category)
                await send_html_message(digest)
                logger.info(f"📬 Дайджест для '{category}' надіслано")
            else:
                logger.info(f"⏭️ Категорія '{category}' не відправлена (немає контенту або перевищено ліміт)")
        except Exception as e:
            logger.exception(f"💥 Помилка в llm_worker: {e}")
        finally:
            # Інакше llm_queue.join() чекатиме вічно, і cron зависне до таймауту
            llm_queue.task_done()

async def main() -> None:
    await start_client()

    worker_task = asyncio.create_task(llm_worker())
    digest_task = asyncio.create_task(run_digest_threads())

    await digest_task
    await llm_queue.join()
    worker_task.cancel()


    await close_client()
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
