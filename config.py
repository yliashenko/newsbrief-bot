import os

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
bot_token = os.environ["BOT_TOKEN"]
openai_api_key = os.environ["GROQ_API_KEY"]
chat_id = int(os.environ["CHAT_ID"])

# Тематичні потоки: "ai", "psychology", "crypto"
channel_streams = {
    "ai": [
        "@denissexy",
        "@imatrofAI",
        "@seeallochnaya",
        "@ppprompt",
    ],
    "intresting": [
        "@spekamedia",
        "@iSIGHTmedia",
        "@wallstreetukr",
        "@MichaelPatsan",
        "@theworldisnoteasy",
        "@keddr",
    ],
    "crypto": [
        "@crypto_rostik",
    ],
    "politics": [
        "@OstanniyCapitalist",
        "@resurgammmm",
    ]
}