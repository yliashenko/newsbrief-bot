import re
from html import unescape

def sanitize_post_text(text: str) -> str:
    if not text:
        return ""

    text = unescape(text)                        # &amp; → &
    text = re.sub(r"<[^>]+>", "", text)          # Видалення HTML-тегів
    text = re.sub(r"http\S+", "", text)          # Видалення посилань
    text = re.sub(r"[@#]\w+", "", text)          # Видалення @mentions та #hashtags
    text = re.sub(r"\s+", " ", text).strip()     # Обрізання зайвих пробілів
    return text