import requests
import time
from config import GROQ_API_KEY, DEFAULT_MODEL, FALLBACK_MODEL, MAX_RETRIES
from logger import logger

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def summarize_texts(posts: list, model: str = DEFAULT_MODEL, attempt=1) -> list:
    """
    Генерує список саммарі для кожного поста.
    Підтримує fallback-модель та retry-механізм.
    """
    texts = [post["text"] for post in posts if post.get("text")]
    if not texts:
        logger.warning("📭 У постах немає тексту")
        return [{"title": "❌ Немає тексту", "summary": "Пост порожній або недоступний"}]

    prompt = build_prompt(texts)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Стисло підсумуй кожен із наведених постів. Додай заголовок і короткий опис."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        start_time = time.time()
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=HEADERS, json=payload)
        duration = time.time() - start_time

        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]
        logger.info(f"✅ Groq відповідь ({model}) за {duration:.2f}с")
        return parse_summaries(result, len(texts))

    except Exception as e:
        logger.warning(f"⚠️ [Спроба {attempt}] Groq помилка для моделі {model}: {e}")

        if attempt < MAX_RETRIES:
            time.sleep(2 * attempt)  # експоненціальна затримка
            return summarize_texts(posts, model=model, attempt=attempt + 1)

        elif model != FALLBACK_MODEL:
            logger.warning(f"🔁 Переходимо на fallback-модель: {FALLBACK_MODEL}")
            return summarize_texts(posts, model=FALLBACK_MODEL, attempt=1)

        else:
            logger.error("❌ Не вдалося згенерувати саммарі навіть з fallback-моделлю.")
            return [{"title": "❌ Помилка", "summary": "Не вдалося згенерувати дайджест"}]

def build_prompt(texts: list) -> str:
    return "\n\n".join([f"{i+1}. {text.strip()}" for i, text in enumerate(texts)])

def parse_summaries(response_text: str, expected_count: int) -> list:
    """
    Спліт тексту від LLM на окремі блоки з заголовком і саммарі.
    """
    summaries = response_text.strip().split("\n\n")
    parsed = []

    for s in summaries:
        lines = s.strip().split("\n", 1)
        title = lines[0].strip() if len(lines) > 0 else "Без назви"
        summary = lines[1].strip() if len(lines) > 1 else ""
        parsed.append({"title": title, "summary": summary})

    while len(parsed) < expected_count:
        parsed.append({"title": "❌ Пропущено", "summary": "LLM не повернула саммарі."})

    return parsed[:expected_count]