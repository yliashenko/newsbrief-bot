from config import BOT_TOKEN
from aiogram import Bot

if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN must not be None")

bot = Bot(token=BOT_TOKEN)