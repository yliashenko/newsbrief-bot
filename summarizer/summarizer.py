from config import DEFAULT_MODEL
from summarizer.prompt_builder import build_prompt
from summarizer.parser import parse_summaries
from summarizer.llm_client import call_llm
from summarizer.sanitizer import sanitize_post_text
from shared.custom_types import TelegramPost, Summary
import asyncio

async def summarize_post(post: TelegramPost, model: str = DEFAULT_MODEL) -> Summary:
    sanitized = sanitize_post_text(post.get("text", ""))
    if not sanitized:
        return {"title": "❌", "summary": "Пост порожній або некоректний."}
    text = sanitized
    prompt = build_prompt([text])
    response = await call_llm(prompt, model=model)
    if not response.strip():
        return {"title": "❌", "summary": "LLM не повернула відповідь."}
    parsed = parse_summaries(response, expected_count=1)
    return parsed[0] if parsed else {"title": "❌", "summary": "Не вдалося розпарсити."}

async def summarize_text(post: TelegramPost, model: str = DEFAULT_MODEL) -> Summary:
    return await summarize_post(post, model=model)