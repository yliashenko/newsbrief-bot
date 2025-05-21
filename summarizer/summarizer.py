from config import DEFAULT_MODEL
from summarizer.prompt_builder import build_prompt
from summarizer.parser import parse_summaries
from summarizer.llm_client import call_llm
from summarizer.sanitizer import sanitize_post_text

async def summarize_texts(posts: list, model: str = DEFAULT_MODEL) -> list:
    if not posts:
        return [{"title": "⚠️ Немає постів", "summary": "Не було знайдено нових повідомлень для аналізу."}]

    texts = [sanitize_post_text(p["text"]) for p in posts if p.get("text")]
    prompt = build_prompt(texts)
    response_text = await call_llm(prompt, model=model)
    return parse_summaries(response_text, expected_count=len(posts))