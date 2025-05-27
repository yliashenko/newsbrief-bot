import re
from html import unescape

def sanitize_post_text(text: str) -> str | None:
    if not text:
        return None

    # Перевірка на наявність 16-значного номера картки
    if re.search(r"(?:\d[ -]*?){16}", text):
        return None

    text = unescape(text)                        # &amp; → &
    text = re.sub(r"<[^>]+>", "", text)          # Видалення HTML-тегів
    text = re.sub(r"http\S+", "", text)          # Видалення посилань
    text = re.sub(r"[@#]\w+", "", text)          # Видалення @mentions та #hashtags
    text = re.sub(r"[•▪︎◦●‣♦❖▶➤➥➔→➢➣➤➧➨➩➪➫➬➭➮➯]", "", text)  # Видалення маркерів списку
    text = re.sub(r"\s+", " ", text).strip()     # Обрізання зайвих пробілів

    return text