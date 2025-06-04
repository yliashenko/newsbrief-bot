import aiohttp
import asyncio
import time
from config import (
    GROQ_API_KEY,
    DEFAULT_MODEL,
    FALLBACK_MODEL,
    MAX_RETRIES,
    SYSTEM_PROMPT,
    RATE_LIMIT_INTERVAL,
)
from shared.logger import logger

rate_limit_lock = asyncio.Lock()
_last_request_time = 0.0

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

async def call_llm(prompt: str, model: str = DEFAULT_MODEL, attempt: int = 1) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        async with rate_limit_lock:
            global _last_request_time
            elapsed = time.time() - _last_request_time
            if elapsed < RATE_LIMIT_INTERVAL:
                await asyncio.sleep(RATE_LIMIT_INTERVAL - elapsed)
            _last_request_time = time.time()

        start_time = time.time()
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=HEADERS,
                json=payload
            ) as response:

                duration = time.time() - start_time
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"{response.status} {response.reason}: {error_text}")
                data = await response.json()

        logger.info(f"✅ Groq відповідь ({model}) за {duration:.2f}с")
        return str(data["choices"][0]["message"]["content"])

    except asyncio.TimeoutError:
        logger.warning(f"⏳ [Спроба {attempt}] Таймаут очікування відповіді від LLM.")
        if attempt < MAX_RETRIES:
            return await call_llm(prompt, model=model, attempt=attempt + 1)
        elif model != FALLBACK_MODEL:
            logger.warning(f"🔁 Переходимо на fallback-модель: {FALLBACK_MODEL}")
            return await call_llm(prompt, model=FALLBACK_MODEL, attempt=1)
        else:
            logger.error("❌ Не вдалося згенерувати відповідь навіть з fallback-моделлю.")
            return "❌ Помилка. Таймаут запиту до LLM."

    except Exception as e:
        logger.warning(f"⚠️ [Спроба {attempt}] Groq помилка для моделі {model}: {e}")

        if attempt < MAX_RETRIES:
            return await call_llm(prompt, model=model, attempt=attempt + 1)

        elif model != FALLBACK_MODEL:
            logger.warning(f"🔁 Переходимо на fallback-модель: {FALLBACK_MODEL}")
            return await call_llm(prompt, model=FALLBACK_MODEL, attempt=1)

        else:
            logger.error("❌ Не вдалося згенерувати відповідь навіть з fallback-моделлю.")
            return "❌ Помилка. Не вдалося згенерувати відповідь."
