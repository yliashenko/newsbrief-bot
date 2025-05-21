from summarizer import summarize_texts
from logger import logger

MAX_MESSAGE_LENGTH = 4096  # Ліміт повідомлення Telegram

def format_digest(category: str, posts: list, emoji: str) -> str | None:
    """
    Формує HTML дайджест для однієї категорії.
    Якщо постів немає — повертає None.
    """
    if not posts:
        logger.warning(f"🔕 Пропущено категорію '{category}' — постів немає.")
        return None

    summaries = summarize_texts(posts)

    result = [f"📚 Зведення по темі: <b>{category}</b>"]
    total_length = len(result[0]) + 2  # початковий заголовок + запас

    for i, (post, summary) in enumerate(zip(posts, summaries), start=1):
        block = (
            f"<b>{i}. {emoji} {summary['title']}</b>\n"
            f"{summary['summary']}\n"
            f'<a href="{post["url"]}">Читати пост</a>\n'
            f'— — —'
        )

        if total_length + len(block) > MAX_MESSAGE_LENGTH:
            logger.warning(f"✂️ Дайджест '{category}' досяг ліміту символів. Зупинка на {i} постах.")
            break

        result.append(block)
        total_length += len(block)

    return "\n".join(result)