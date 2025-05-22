# bot_handlers.py

import json
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import CHANNEL_GROUPS

router = Router()

# Функції для роботи з JSON
def load_channel_groups():
    with open(CHANNEL_GROUPS, "r", encoding="utf-8") as f:
        return json.load(f)

def save_channel_groups(data):
    with open(CHANNEL_GROUPS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Стан машини
class AddChannelStates(StatesGroup):
    choosing_group = State()
    entering_channel = State()

# /addchannel
@router.message(F.text == "/addchannel")
async def cmd_addchannel(message: types.Message, state: FSMContext):
    groups = list(load_channel_groups().keys())
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=g)] for g in groups],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Оберіть потік, до якого хочете додати канал:", reply_markup=keyboard)
    await state.set_state(AddChannelStates.choosing_group)

# вибір потоку
@router.message(AddChannelStates.choosing_group)
async def process_group_choice(message: types.Message, state: FSMContext):
    group = message.text
    groups = load_channel_groups()
    if group not in groups:
        await message.answer("❌ Такого потоку не існує. Спробуйте ще раз.")
        return
    await state.update_data(group=group)
    await message.answer("Введіть нікнейм Telegram-каналу (наприклад, @example):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddChannelStates.entering_channel)

# додавання каналу
@router.message(AddChannelStates.entering_channel)
async def process_channel_entry(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group = data["group"]
    nickname = message.text.strip()

    if not nickname.startswith("@"):
        await message.answer("❌ Нікнейм має починатися з @. Спробуйте ще раз.")
        return

    groups = load_channel_groups()

    if nickname in groups[group]:
        await message.answer("✅ Цей канал вже є у списку.")
    else:
        groups[group].append(nickname)
        save_channel_groups(groups)
        await message.answer(f"✅ Канал {nickname} додано до потоку {group}.")

    await state.clear()