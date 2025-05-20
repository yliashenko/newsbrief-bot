from telethon import TelegramClient
from config import API_ID, API_HASH

async def get_channel_posts(channels: list[str], limit=10):
    result = {}
    async with TelegramClient("user_session", API_ID, API_HASH) as client:
        for channel in channels:
            try:
                messages = await client.get_messages(channel, limit=limit)
                enriched = [
                    {
                        "text": m.message,
                        "id": m.id,
                        "channel_id": m.peer_id.channel_id if hasattr(m.peer_id, "channel_id") else None
                    }
                    for m in messages if hasattr(m, 'message') and m.message
                ]
                result[channel] = enriched
            except Exception as e:
                result[channel] = [
                    {
                        "text": f"⚠️ Не вдалося отримати повідомлення з {channel}: {e}",
                        "id": None,
                        "channel_id": None
                    }
                ]
    return result


async def get_channel_title(channel: str) -> str:
    async with TelegramClient("user_session", API_ID, API_HASH) as client:
        try:
            entity = await client.get_entity(channel)
            return entity.title
        except Exception:
            return channel  # fallback до username, якщо назву не вдалося отримати