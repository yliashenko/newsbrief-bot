from telethon.sync import TelegramClient
from config import API_ID, API_HASH
from telethon.tl.types import Message

# Ініціалізація клієнта один раз
client = TelegramClient("user_session", API_ID, API_HASH)

async def get_channel_posts(channel_username: str, limit: int = 20) -> list:
    """
    Отримує останні повідомлення з каналу та повертає список словників:
    { id, text, url }
    """
    async with client:
        try:
            messages = await client.get_messages(channel_username, limit=limit)
            return [
                {
                    "id": msg.id,
                    "text": msg.message,
                    "url": f"https://t.me/{channel_username.strip('@')}/{msg.id}"
                }
                for msg in messages if msg.message
            ]
        except Exception as e:
            print(f"⚠️ Не вдалося отримати повідомлення з {channel_username}: {e}")
            return []

async def get_channel_title(channel: str) -> str:
    """
    Отримує повну назву каналу по username.
    Повертає username як fallback у разі помилки.
    """
    async with TelegramClient("user_session", API_ID, API_HASH) as client:
        try:
            entity = await client.get_entity(channel)
            return entity.title
        except Exception:
            return channel  # fallback до username