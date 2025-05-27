from typing import List
from shared.custom_types import Summary

def parse_summaries(response_text: str, expected_count: int) -> List[Summary]:
    summaries = response_text.strip().split("\n\n")
    parsed: List[Summary] = []

    for s in summaries:
        lines = s.strip().split("\n", 1)
        title = lines[0].strip() if lines else ""
        summary = lines[1].strip() if len(lines) > 1 else ""

        if not title and not summary:
            parsed.append(Summary(
                title="❌",
                summary="LLM не повернула відповідь. Можливі причини: rate limit або надто великий prompt."
            ))
        else:
            parsed.append(Summary(
                title=title,
                summary=summary
            ))

    while len(parsed) < expected_count:
        parsed.append(Summary(
            title="❌",
            summary="LLM не повернула відповідь."
        ))

    return parsed[:expected_count]