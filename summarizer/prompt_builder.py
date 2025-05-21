def build_prompt(texts: list) -> str:
    return "\n\n".join([f"{i+1}. {text.strip()}" for i, text in enumerate(texts)])