from summarizer import summarize_texts
from logger import logger

async def format_digest(category: str, posts: list, emoji: str) -> str:
    if not posts:
        logger.warning(f"🔕 Пропущено категорію '{category}' — постів немає.")
        return ""

    summaries = await summarize_texts(posts)

    result = [f"📚 Зведення по темі: <b>{category.upper()}</b>\n"]
    total_length = 0

    for i, (post, summary) in enumerate(zip(posts, summaries), start=1):
        block = (
            f"<b>{i}. {emoji} {summary['title']}</b>\n"
            f"{summary['summary']}\n"
            f'<a href="{post["url"]}">Читати пост</a>\n'
            f'— — —'
        )
        block_len = len(block)
        if total_length + block_len > 4096:
            logger.warning(f"✂️ Дайджест '{category}' досяг ліміту символів. Зупинка на {i} постах.")
            break
        result.append(block)
        total_length += block_len

    return "\n".join(result)