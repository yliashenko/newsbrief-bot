from summarizer import summarize_texts
from logger import logger
import re

async def format_digest(category: str, posts: list, emoji: str) -> str:
    if not posts:
        logger.warning(f"🔕 Пропущено категорію '{category}' — постів немає.")
        return ""

    summaries = await summarize_texts(posts)

    result = [f"📚 Зведення по темі: <b>{category.upper()}</b>\n"]
    total_length = 0

    for i, (post, summary) in enumerate(zip(posts, summaries), start=1):
        title = clean_summary_text(summary["title"])
        summary_text = clean_summary_text(summary["summary"])

        block = (
            f"<b>{i}. {emoji} {title}</b>\n"
            f"{summary_text}\n"
            f'<a href="https://t.me/{post["channel"]}/{post["id"]}">Читати пост</a>\n'
            f'\n\n'
        )
        block_len = len(block)
        if total_length + block_len > 4096:
            logger.warning(f"✂️ Дайджест '{category}' досяг ліміту символів. Зупинка на {i} постах.")
            break
        result.append(block)
        total_length += block_len

    return "\n".join(result)

def clean_summary_text(text: str) -> str:
    text = re.sub(r'(?<!\*)\*\*(.*?)\*\*(?!\*)', r'<b>\1</b>', text)  # **bold** → <b>
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)  # remove heading #
    text = re.sub(r'^-\s*', '• ', text, flags=re.MULTILINE)  # - point → • point
    return text.strip()
