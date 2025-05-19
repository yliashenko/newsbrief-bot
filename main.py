import asyncio
from telegram_client import get_channel_posts
from summarizer import summarize_texts
from aiogram import Bot
from config import bot_token, chat_id, channel_streams

async def main():
    bot = Bot(token=bot_token)

    for stream_name, channels in channel_streams.items():
        posts_by_channel = await get_channel_posts(channels=channels, limit=10)

        result = f"\U0001F4DA Зведення по темі: *{stream_name.upper()}*\n"

        for channel, posts in posts_by_channel.items():
            texts = [p.message for p in posts if hasattr(p, 'message') and p.message][:5]
            try:
                summary = await summarize_texts(texts)
                result += f"\n\U0001F4CC *{channel}*:\n{summary.strip()}\n"
            except Exception as e:
                result += f"\n⚠️ {channel}: Помилка при обробці — {e}\n"

            await asyncio.sleep(7)  # throttle for Groq rate limits

        await bot.send_message(chat_id=chat_id, text=result[:4000], parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
