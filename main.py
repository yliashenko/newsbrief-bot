import asyncio
from telegram_client import get_channel_posts
from summarizer import summarize_texts
from aiogram import Bot
from config import bot_token, chat_id

async def main():
    posts_by_channel = await get_channel_posts(limit=10)

    result = "📅 Зведення новин:\n"
    bot = Bot(token=bot_token)

    for channel, posts in posts_by_channel.items():
        texts = [p.message for p in posts if p.message][:5]  # ✂️ обрізаємо кількість постів
        summary = await summarize_texts(texts)
        result += f"\n📌 {channel}:\n{summary.strip()}\n"

        await asyncio.sleep(7)

    await bot.send_message(chat_id=chat_id, text=result[:4000])

if __name__ == "__main__":
    asyncio.run(main())