from config import DEFAULT_MODEL, MAX_POSTS_PER_REQUEST
from summarizer.prompt_builder import build_prompt
from summarizer.parser import parse_summaries
from summarizer.llm_client import call_llm
from summarizer.sanitizer import sanitize_post_text

async def summarize_texts(posts: list, model: str = DEFAULT_MODEL) -> list:
    if not posts:
        return [{"title": "⚠️ Немає постів", "summary": "Не було знайдено нових повідомлень для аналізу."}]

    cleaned_pairs = [
        (p, sanitize_post_text(p["text"]))
        for p in posts if p.get("text")
    ]
    cleaned_pairs = cleaned_pairs[:MAX_POSTS_PER_REQUEST]
    if not cleaned_pairs:
        return [{"title": "❌", "summary": "LLM не повернула відповідь."}]

    posts, texts = zip(*cleaned_pairs)
    prompt = build_prompt(list(texts))
    response_text = await call_llm(prompt, model=model)

    if not response_text.strip():
        return [{"title": "❌", "summary": "LLM не повернула відповідь."}]

    if response_text.strip().startswith("❌"):
        return [{"title": "❌", "summary": "LLM не повернула відповідь."}]

    summaries = parse_summaries(response_text, expected_count=len(posts))
    return [{"title": s.title.strip(), "summary": s.summary.strip()} for s in summaries[:len(posts)] if s.title.strip() or s.summary.strip()]