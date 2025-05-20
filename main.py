import asyncio
from telegram_client import get_channel_posts, get_channel_title
from summarizer import summarize_texts, generate_title
from aiogram import Bot
from config import bot_token, chat_id, channel_groups
import html

def escape_html(text: str) -> str:
    return html.escape(text)

async def main():
    bot = Bot(token=bot_token, parse_mode="HTML")
    try:
        for group_name, channels in channel_groups.items():
            result = f"📚 <b>Зведення по темі: {escape_html(group_name.upper())}</b>\n\n"
            for channel in channels:
                try:
                    posts = await get_channel_posts(channel, limit=5)
                    texts = [p.message for p in posts if p.message]
                    if not texts:
                        raise ValueError("Немає повідомлень")

                    title = await get_channel_title(channel)
                    result += f"📌 <b>{escape_html(title)}</b>:\n"

                    for i, text in enumerate(texts, start=1):
                        summary = await summarize_texts([text])
                        headline = await generate_title(text)

                        post_link = posts[i - 1].link if hasattr(posts[i - 1], 'link') else None
                        if post_link:
                            result += f'{i}.🧠 <a href="{post_link}">{escape_html(headline)}</a>:\n{escape_html(summary.strip())}\n\n'
                        else:
                            result += f'{i}.🧠 <b>{escape_html(headline)}</b>:\n{escape_html(summary.strip())}\n\n'
                except Exception as e:
                    result += f"❌ Помилка при обробці {escape_html(channel)}: {escape_html(str(e))}\n\n"

            await bot.send_message(chat_id=chat_id, text=result[:4000])
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())