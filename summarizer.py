import openai

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"
)

async def summarize_texts(texts):
    prompt = (
        "Ось добірка повідомлень з Telegram. "
        "Сформуй коротке зведення (2–5 тез українською):\n\n" + "\n\n".join(texts)
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Ти аналітик новин. Формуй короткі дайджести."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.7,
    )

    return response.choices[0].message.content