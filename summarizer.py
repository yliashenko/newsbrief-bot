import openai
import os

openai.api_key = os.environ["GROQ_API_KEY"]
openai.api_base = "https://api.groq.com/openai/v1"

async def summarize_texts(texts):
    prompt = (
        "Ось добірка повідомлень з Telegram. "
        "Сформуй коротке зведення (2–5 тез українською):\n\n" + "\n\n".join(texts)
    )

    response = openai.ChatCompletion.create(
        model="mistral-saba-24b",
        messages=[
            {"role": "system", "content": "Ти аналітик новин. Формуй короткі дайджести."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.7,
    )

    return response["choices"][0]["message"]["content"]