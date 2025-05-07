from telethon import TelegramClient
from config import api_id, api_hash, channel_usernames

# Авторизація через звичайний акаунт
client = TelegramClient("user_session", api_id, api_hash)

async def get_channel_posts(limit=10):
    await client.start()  # ← Тут тебе попросять ввести номер телефону + код
    posts_by_channel = {}
    for channel in channel_usernames:
        messages = await client.get_messages(channel, limit=limit)
        posts_by_channel[channel] = messages
    return posts_by_channel