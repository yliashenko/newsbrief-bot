import asyncio
import re
from telegram_client import get_channel_posts
from summarizer import summarize_texts, generate_title
from aiogram import Bot
from config import bot_token, chat_id, channel_streams

def escape_markdown(text):
    # Екрануємо лише символи, які обов'язково треба екранувати у MarkdownV2
    return re.sub(r'([_\*\[\]\(\)~`>#+=|{}!\-])', r'\\\1', text)

def build_bold_linked_title(title: str, channel_id: int, message_id: int) -> str:
    escaped_title = escape_markdown(title)
    if channel_id and message_id:
        chat_link = f"https://t.me/c/{channel_id}/{message_id}"
        return f"[{escaped_title}]({chat_link})"
    return escaped_title

async def main():
    bot = Bot(token=bot_token)

    for stream_name, channels in channel_streams.items():
        posts_by_channel = await get_channel_posts(channels=channels, limit=10)

        result = f"\U0001F4DA Зведення по темі: *{escape_markdown(stream_name.upper())}*\n"
        empty_stream = True

        for channel, posts in posts_by_channel.items():
            channel_title = None
            for post in posts:
                if post.get("channel_title"):
                    channel_title = post.get("channel_title")
                    break
            channel_label = escape_markdown(channel_title or channel)

            result += f"\n\U0001F4CC *{channel_label}*:\n"

            if not posts:
                result += f"⚠️ Неможливо отримати пости з {channel_label}\n"
                continue

            try:
                for idx, post in enumerate(posts[:5]):
                    text = post.get("text")
                    channel_id = post.get("channel_id")
                    message_id = post.get("id")

                    if not text:
                        continue

                    title = await generate_title(text)
                    summary = await summarize_texts([text])

                    summary = summary.strip()
                    if len(summary) > 700:
                        summary = summary[:700].rsplit(".", 1)[0] + "."

                    summary = re.sub(r"(?i)^\*+Зведення з Telegram:?\*+", "", summary).strip()
                    summary = re.sub(r"\n\d+[\)\.\-]", ".", summary).strip()
                    summary = re.sub(r"\n+", " ", summary)

                    emoji = "🤖" if "ai" in stream_name.lower() else "🧠"
                    title_link = build_bold_linked_title(title, channel_id, message_id)
                    prefix = escape_markdown(f"{idx+1}\.{emoji}")

                    result += f"{prefix} {title_link}:\n{escape_markdown(summary)}\n\n"

                empty_stream = False
            except Exception as e:
                result += f"⚠️ Помилка при обробці {channel_label}: {escape_markdown(str(e))}\n"

            await asyncio.sleep(7)

        if empty_stream:
            result += "\n⚠️ У цьому потоці не вдалося сформувати жодного зведення.\n"

        if len(result) > 4000:
            result = result[:3995] + "..."

        await bot.send_message(chat_id=chat_id, text=result, parse_mode="MarkdownV2")

if __name__ == "__main__":
    asyncio.run(main())
