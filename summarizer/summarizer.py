from config import DEFAULT_MODEL, MAX_POSTS_PER_REQUEST
from summarizer.prompt_builder import build_prompt
from summarizer.parser import parse_summaries
from summarizer.llm_client import call_llm
from summarizer.sanitizer import sanitize_post_text
import asyncio

async def summarize_post(post: dict, model: str = DEFAULT_MODEL) -> dict:
    text = sanitize_post_text(post.get("text", ""))
    if not text:
        return {"title": "❌", "summary": "Пост порожній або некоректний."}
    prompt = build_prompt([text])
    response = await call_llm(prompt, model=model)
    if not response.strip():
        return {"title": "❌", "summary": "LLM не повернула відповідь."}
    parsed = parse_summaries(response, expected_count=1)
    return parsed[0] if parsed else {"title": "❌", "summary": "Не вдалося розпарсити."}

async def summarize_text(posts: list, model: str = DEFAULT_MODEL) -> list:
    if not posts:
        return [{"title": "⚠️ Немає постів", "summary": "Не було знайдено нових повідомлень для аналізу."}]
    semaphore = asyncio.Semaphore(5)

    async def limited(post):
        async with semaphore:
            return await summarize_post(post, model)

    posts = posts[:MAX_POSTS_PER_REQUEST]
    return await asyncio.gather(*(limited(p) for p in posts))