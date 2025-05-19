from telethon import TelegramClient
from config import api_id, api_hash

async def get_channel_posts(channels: list[str], limit=10):
    result = {}
    async with TelegramClient("user_session", api_id, api_hash) as client:
        for channel in channels:
            try:
                messages = await client.get_messages(channel, limit=limit)
                result[channel] = messages
            except Exception as e:
                result[channel] = [type("Error", (object,), {"message": f"⚠️ Не вдалося отримати повідомлення з {channel}: {e}"})()]
    return result
