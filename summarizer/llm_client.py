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

# Переконаємося що ключ очищений від зайвих символів
_clean_api_key = GROQ_API_KEY.strip() if GROQ_API_KEY else None

# Діагностика: логуємо звідки завантажується ключ
logger.info(f"🔑 GROQ_API_KEY в llm_client: {_clean_api_key[:8]}...{_clean_api_key[-8:] if _clean_api_key else 'N/A'} (довжина: {len(_clean_api_key) if _clean_api_key else 0})")
# Перевірка чи це правильний ключ
if _clean_api_key and not _clean_api_key.startswith("gsk_sJXF"):
    logger.warning(f"⚠️  УВАГА: Використовується ключ, який не відповідає очікуваному!")
    logger.warning(f"   Очікується: gsk_sJXF...")
    logger.warning(f"   Використовується: {_clean_api_key[:8]}...")

HEADERS = {
    "Authorization": f"Bearer {_clean_api_key}",
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
                    # Детальна обробка помилки 401 (Invalid API Key)
                    if response.status == 401:
                        logger.error("❌ GROQ_API_KEY невалідний!")
                        # Діагностична інформація (без повного ключа)
                        if _clean_api_key:
                            logger.error(f"   Довжина ключа: {len(_clean_api_key)} символів")
                            logger.error(f"   Починається з: {_clean_api_key[:8]}...")
                            logger.error(f"   Закінчується на: ...{_clean_api_key[-8:]}")
                        else:
                            logger.error("   Ключ порожній або не завантажився!")
                        logger.error("💡 Перевірте:")
                        logger.error("   1. Чи правильно скопійований ключ з https://console.groq.com/keys")
                        logger.error("   2. Чи немає зайвих пробілів на початку/кінці ключа")
                        logger.error("   3. Чи встановлено ключ в Environment Variables на Render")
                        logger.error("   4. Перезапустіть сервіс після зміни ключа на Render")
                        logger.error(f"   5. Деталі помилки: {error_text}")
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
