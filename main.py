import asyncio
import re
from telegram_client import get_channel_posts
from summarizer import summarize_texts
from aiogram import Bot
from config import bot_token, chat_id, channel_streams

def escape_markdown(text):
    return re.sub(r'([_\*\[\]\(\)~`>#+\-=|{}.!])', r'\\\1', text)

async def main():
    bot = Bot(token=bot_token)

    for stream_name, channels in channel_streams.items():
        posts_by_channel = await get_channel_posts(channels=channels, limit=10)

        result = f"\U0001F4DA Зведення по темі: *{stream_name.upper()}*\n"
        empty_stream = True

        for channel, posts in posts_by_channel.items():
            texts = [p.message for p in posts if hasattr(p, 'message') and p.message][:5]

            if not texts:
                result += f"\n⚠️ Неможливо отримати пости з {channel}\n"
                continue

            try:
                summary = await summarize_texts(texts)
                result += f"\n\U0001F4CC *{channel}*:\n{summary.strip()}\n"
                empty_stream = False
            except Exception as e:
                result += f"\n⚠️ Помилка при обробці {channel}: {e}\n"

            await asyncio.sleep(7)

        if empty_stream:
            result += "\n⚠️ У цьому потоці не вдалося сформувати жодного зведення.\n"

        escaped_result = escape_markdown(result)
        await bot.send_message(chat_id=chat_id, text=escaped_result[:4000], parse_mode="MarkdownV2")

if __name__ == "__main__":
    asyncio.run(main())
