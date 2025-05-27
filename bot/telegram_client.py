from telethon import TelegramClient
from telethon.tl.types import Channel
from config import API_ID, API_HASH
from shared.logger import logger

client = TelegramClient("user_session", API_ID, API_HASH)

# Стартуємо клієнт при запуску застосунку
async def start_client() -> None:
    if not client.is_connected():
        await client.connect()
    if not await client.is_user_authorized():
        raise RuntimeError("❌ Телеграм клієнт не авторизований")

async def get_channel_posts(channel_username: str, limit: int = 20) -> list[dict[str, str | int]]:
    if not client.is_connected():
        await client.connect()
    try:
        messages = await client.get_messages(channel_username, limit=limit)
        return [
            {
                "id": msg.id,
                "text": msg.message,
                "url": f"https://t.me/{channel_username.strip('@')}/{msg.id}",
                "channel": channel_username.strip('@')
            }
            for msg in messages if msg.message
        ]
    except Exception as e:
        logger.warning(f"⚠️ Не вдалося отримати повідомлення з {channel_username}: {e}")
        return []

async def get_channel_title(channel: str) -> str:
    title: str
    try:
        entity = await client.get_entity(channel)
        if isinstance(entity, Channel) and entity.title:
            title = entity.title
        else:
            title = channel
    except Exception:
        title = channel
    return title
async def close_client() -> None:
    if client.is_connected():
        await client.disconnect()