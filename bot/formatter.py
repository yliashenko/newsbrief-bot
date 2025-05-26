from config import POST_ENTRY_EMOJI
from shared.types import TelegramPost, SummaryEntry
from summarizer.summarizer import summarize_text
from shared.logger import logger
import re

async def format_digest(category: str, posts: list[TelegramPost], emoji: str) -> str:
    if not posts:
        logger.warning(f"🔕 Пропущено категорію '{category}' — постів немає.")
        return ""

    logger.info(f"🌀 Починається обробка {len(posts)} постів у категорії {category}")

    summaries: list[SummaryEntry] = []
    for post in posts:

        logger.info(f"🔄 summarize_text start: {post['channel']}/{post['id']}")
        summary = await summarize_text(post)
        logger.info(f"✅ summarize_text done: {post['channel']}/{post['id']}")
        
        if summary is None:
            summary = {"title": "", "summary": ""}
        summaries.append(summary)

    result = [format_title(category, emoji)]
    total_length = len(result[0])

    for i, (post, summary) in enumerate(zip(posts, summaries), start=1):
        title = clean_summary_text(summary["title"])
        summary_text = clean_summary_text(summary["summary"])
        url = f"https://t.me/{post['channel']}/{post['id']}"
        if not title and not summary_text:
            entry_block = f"<b>{POST_ENTRY_EMOJI} ❌</b>\nLLM не повернула відповідь.\n<a href=\"{url}\">Читати пост →</a>\n"
        else:
            entry_block = format_entry(i, title, summary_text, url)
        block_len = len(entry_block)
        if total_length + block_len > 4096:
            logger.warning(f"✂️ Дайджест '{category}' досяг ліміту символів. Зупинка на {i} постах.")
            break
        result.append(entry_block)
        total_length += block_len

    result.append(format_footer())
    return "\n".join(result)

def format_title(category: str, emoji: str) -> str:
    return f"<b>{category.upper()} {emoji}</b>\n"

def format_entry(index: int, title: str, summary: str, url: str) -> str:
    return (
        f"<b>{POST_ENTRY_EMOJI} {title}</b>\n"
        f"{summary}\n"
        f'<a href="{url}">Читати пост →</a>\n'
    )

def format_footer() -> str:
    return "\n<i>Згенеровано ботом ✨</i>"

def clean_summary_text(text: str) -> str:
    text = re.sub(r'(?<!\*)\*\*(.*?)\*\*(?!\*)', r'<b>\1</b>', text)  # **bold** → <b>
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)  # remove heading #
    text = re.sub(r'^-\s*', '• ', text, flags=re.MULTILINE)  # - point → • point
    return text.strip()
