from shared.types import TelegramPost, SummaryEntry
from summarizer.summarizer import summarize_texts
from shared.logger import logger
import re

async def format_digest(category: str, posts: list[TelegramPost], emoji: str) -> str:
    if not posts:
        logger.warning(f"🔕 Пропущено категорію '{category}' — постів немає.")
        return ""

    summaries: list[SummaryEntry] = await summarize_texts(posts)

    result = [format_title(category, emoji)]
    total_length = len(result[0])

    for i, (post, summary) in enumerate(zip(posts, summaries), start=1):
        title = clean_summary_text(summary["title"])
        summary_text = clean_summary_text(summary["summary"])
        url = f"https://t.me/{post['channel']}/{post['id']}"

        block = format_entry(i, title, summary_text, url)
        block_len = len(block)
        if total_length + block_len > 4096:
            logger.warning(f"✂️ Дайджест '{category}' досяг ліміту символів. Зупинка на {i} постах.")
            break
        result.append(block)
        total_length += block_len

    result.append(format_footer())
    return "\n".join(result)

def format_title(category: str, emoji: str) -> str:
    return f"{emoji} Що нового: <b>{category.upper()}</b>\n"

def format_entry(index: int, title: str, summary: str, url: str) -> str:
    return (
        f"<b>{index}. {title}</b>\n"
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
