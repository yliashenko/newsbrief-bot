import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from chat_bot_ui.bot_handlers import router
from chat_bot_ui.bot_menu import menu_router
from config import BOT_TOKEN

async def start_bot():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    dp.include_router(menu_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())