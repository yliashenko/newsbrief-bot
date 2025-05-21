def parse_summaries(response_text: str, expected_count: int) -> list:
    summaries = response_text.strip().split("\n\n")
    parsed = []

    for s in summaries:
        lines = s.strip().split("\n", 1)
        title = lines[0].strip() if lines[0].strip() else "Без назви"
        summary = (
            lines[1].strip() if len(lines) > 1 and lines[1].strip()
            else "⚠️ LLM не повернула опис для цього поста."
        )
        parsed.append({"title": title, "summary": summary})

    while len(parsed) < expected_count:
        parsed.append({
            "title": "❌ Пропущено",
            "summary": "LLM не повернула саммарі."
        })

    return parsed[:expected_count]