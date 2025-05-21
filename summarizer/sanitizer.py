import re
from html import unescape

def sanitize_post_text(text: str, min_len: int = 150, max_len: int = 1000) -> str:
    if not text:
        return ""

    text = unescape(text)                        # &amp; → &
    text = re.sub(r"<[^>]+>", "", text)          # Видалення HTML-тегів
    text = re.sub(r"http\S+", "", text)          # Видалення посилань
    text = re.sub(r"[@#]\w+", "", text)          # Видалення @mentions та #hashtags
    text = re.sub(r"\s+", " ", text).strip()     # Обрізання зайвих пробілів

    if len(text) < min_len:
        return ""

    if len(text) > max_len:
        # обрізати по словах, щоб уникнути обриву
        words = text.split()
        truncated = ""
        for word in words:
            if len(truncated) + len(word) + 1 > max_len:
                break
            truncated += " " + word if truncated else word
        return truncated.strip()

    return text