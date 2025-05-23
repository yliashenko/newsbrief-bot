from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from chat_bot_ui.bot_handlers import cmd_addchannel
import json
from config import CHANNEL_GROUPS

menu_router = Router()

@menu_router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📌 Додати канал")],
            [KeyboardButton(text="📬 Згенерувати дайджест")],
            [KeyboardButton(text="📋 Список каналів")],
            [KeyboardButton(text="🔄 Повернутись до меню")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer("👋 Вітаю! Оберіть дію нижче:", reply_markup=keyboard)

@menu_router.message(F.text == "📌 Додати канал")
async def handle_add_channel_button(message: types.Message, state: FSMContext):
    await cmd_addchannel(message, state)

@menu_router.message(F.text == "📬 Згенерувати дайджест")
async def handle_digest(message: types.Message):
    await message.answer("🔧 Поки що ця функція в розробці.")

@menu_router.message(F.text == "📋 Список каналів")
async def handle_channel_list(message: types.Message):
    with open(CHANNEL_GROUPS, "r", encoding="utf-8") as f:
        groups = json.load(f)

    text = "📚 <b>Список каналів:</b>\n\n"
    for group, channels in groups.items():
        text += f"<b>{group}</b>:\n" + "\n".join(channels) + "\n\n"

    await message.answer(text, parse_mode="HTML")

@menu_router.message(F.text == "🔄 Повернутись до меню")
async def handle_back_to_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await cmd_start(message)