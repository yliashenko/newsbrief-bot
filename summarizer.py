import aiohttp
import asyncio
import time
from config import GROQ_API_KEY, DEFAULT_MODEL, FALLBACK_MODEL, MAX_RETRIES
from logger import logger

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

async def summarize_texts(posts: list, model: str = DEFAULT_MODEL, attempt=1) -> list:
    texts = [post["text"][:1000] for post in posts if post.get("text")]
    if not texts:
        logger.warning("📭 У постах немає тексту")
        return [{"title": "❌ Немає тексту", "summary": "Пост порожній або недоступний"}]

    prompt = build_prompt(texts)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Ти висококлассний редактор відомого медіа. Стисло підсумуй кожен із наведених постів. Додай заголовок і короткий опис. Укранською мовою"},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        await asyncio.sleep(1.5)  # rate limit protection
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=HEADERS,
                json=payload
            ) as response:
                duration = time.time() - start_time
                if response.status != 200:
                    raise aiohttp.ClientResponseError(
                        status=response.status,
                        message=await response.text()
                    )
                data = await response.json()

        result = data["choices"][0]["message"]["content"]
        logger.info(f"✅ Groq відповідь ({model}) за {duration:.2f}с")
        return parse_summaries(result, len(texts))

    except Exception as e:
        logger.warning(f"⚠️ [Спроба {attempt}] Groq помилка для моделі {model}: {e}")

        if attempt < MAX_RETRIES:
            await asyncio.sleep(2 * attempt)
            return await summarize_texts(posts, model=model, attempt=attempt + 1)

        elif model != FALLBACK_MODEL:
            logger.warning(f"🔁 Переходимо на fallback-модель: {FALLBACK_MODEL}")
            return await summarize_texts(posts, model=FALLBACK_MODEL, attempt=1)

        else:
            logger.error("❌ Не вдалося згенерувати саммарі навіть з fallback-моделлю.")
            return [{"title": "❌ Помилка", "summary": "Не вдалося згенерувати дайджест"}]

def build_prompt(texts: list) -> str:
    return "\n\n".join([f"{i+1}. {text.strip()}" for i, text in enumerate(texts)])

def parse_summaries(response_text: str, expected_count: int) -> list:
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