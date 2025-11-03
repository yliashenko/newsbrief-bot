from telethon import TelegramClient
from telethon.tl.types import Channel
from config import API_ID, API_HASH
from shared.logger import logger

client = TelegramClient("user_session", API_ID, API_HASH)

# Стартуємо клієнт при запуску застосунку
async def start_client() -> None:
    """
    Ініціалізує та авторизує Telegram клієнт.
    Викликає start() для авторизації (якщо сесія валідна, авторизується автоматично).
    Важливо: використовуйте user account (номер телефону), а НЕ bot token!
    """
    try:
        # start() автоматично підключається і авторизує, якщо сесія валідна
        await client.start()
        
        # Перевіряємо, що авторизація пройшла успішно
        if not await client.is_user_authorized():
            raise RuntimeError("❌ Телеграм клієнт не авторизований після start()")
        
        # Перевіряємо, що це НЕ бот (боти не можуть читати канали)
        try:
            me = await client.get_me()
            if hasattr(me, 'bot') and me.bot:
                raise RuntimeError(
                    "❌ Сесія авторизована як бот!\n"
                    "💡 Для читання каналів потрібна user account сесія.\n"
                    "   Видаліть user_session.session і створіть нову сесію з номером телефону (не bot token)"
                )
        except RuntimeError:
            raise
        except Exception as e:
            logger.warning(f"⚠️ Не вдалося перевірити тип акаунта: {e}")
        
        logger.info("✅ Telegram клієнт успішно авторизований як user account")
    except Exception as e:
        logger.error(f"❌ Помилка авторизації Telegram клієнта: {e}")
        raise RuntimeError(f"❌ Телеграм клієнт не авторизований: {e}")

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
async def check_session_validity() -> dict[str, bool | str | int]:
    """
    Перевіряє валідність сесії та повертає інформацію про неї.
    Повертає словник з інформацією про статус сесії.
    """
    result = {
        "is_valid": False,
        "is_authorized": False,
        "is_bot": False,
        "user_id": None,
        "username": None,
        "error": None
    }
    
    try:
        await client.start()
        
        if await client.is_user_authorized():
            result["is_authorized"] = True
            
            try:
                me = await client.get_me()
                result["user_id"] = me.id
                result["username"] = me.username
                result["is_bot"] = me.bot if hasattr(me, 'bot') else False
                
                # Перевіряємо, чи це бот (не можна використовувати для читання каналів)
                if result["is_bot"]:
                    result["error"] = "Сесія авторизована як бот, але для читання каналів потрібна user account сесія"
                    logger.error(f"❌ {result['error']}")
                    logger.error("💡 Видаліть user_session.session і створіть нову сесію з номером телефону (не bot token)")
                else:
                    result["is_valid"] = True
                    logger.info(f"✅ Сесія валідна. Користувач: {me.first_name} (@{me.username or 'немає'})")
            except Exception as e:
                result["error"] = f"Не вдалося отримати інформацію про користувача: {e}"
                logger.warning(f"⚠️ {result['error']}")
        else:
            result["error"] = "Сесія не авторизована"
            logger.warning("⚠️ Сесія не авторизована")
            
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"❌ Помилка перевірки сесії: {e}")
    
    return result

async def close_client() -> None:
    if client.is_connected():
        await client.disconnect()