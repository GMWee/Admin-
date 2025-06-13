from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import random
import string

from src.base.config import CONFIG
from src.base.database import DATABASE
from src.admin.user_settings.function import SETTINGS
from src.admin.pyment_api import pyment_keyboard as kb

router = Router()

class SetState(StatesGroup):
    api_key = State()
    client_id = State()

def generate_api_key_random(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))

async def check_access_message(message: Message):
    if not await SETTINGS.role_message(message):
        await message.answer('*У вас нет доступа к данному боту! Так как вы не являетесь администрацией бота.*', parse_mode="Markdown")
        return False
    return True

async def check_access_callback(callback: CallbackQuery):
    if not await SETTINGS.role_callback(callback):
        await callback.message.edit_text('*У вас нет доступа к данному боту! Так как вы не являетесь администрацией бота.*', parse_mode="Markdown")
        return False
    return True

@router.message(Command("yoomoney"))
async def yoomoney_message(message: Message):
    if not await check_access_message(message):
        return
    await message.answer("*YooMoney menu*", reply_markup=kb.menu, parse_mode="Markdown")

@router.callback_query(F.data == "back_to_yoomoney")
async def yoomoney_callback(callback: CallbackQuery):
    if not await check_access_callback(callback):
        return
    await callback.message.edit_text("*YooMoney menu*", reply_markup=kb.menu, parse_mode="Markdown")

@router.callback_query(F.data == "apikey_add")
async def apikey_add_callback(callback: CallbackQuery, state: FSMContext):
    if not await check_access_callback(callback):
        return
    await callback.message.edit_text('<b>Название сервиса для генерации ключа:</b>', parse_mode='HTML')
    await state.set_state(SetState.api_key)

@router.message(SetState.api_key)
async def apikey_add_message(message: Message, state: FSMContext):
    client = message.text.strip()
    key = generate_api_key_random()
    if await DATABASE.info_api_key(client):
        await message.answer('*Название сервиса для генерации ключа занято*', parse_mode="Markdown")
        return
    await DATABASE.add_api_key(client, key)
    await message.answer(
        f"*Ключ добавлен*\n\nСервис: `{client}`\nКлюч: `{key}` ✅",
        reply_markup=kb.back_to_settings,
        parse_mode="Markdown"
    )
    await state.clear()

@router.callback_query(F.data == "get_tabel")
async def api_key_print(callback: CallbackQuery):
    if not await check_access_callback(callback):
        return

    records = await DATABASE.api_key_print()
    if not records:
        await callback.message.edit_text('*Таблица api_key пуста*', reply_markup=kb.back_to_settings, parse_mode="Markdown")
        return
    text = ""
    for record in records:
        text += (
            f"**Client:** `{record['client']}`\n"
            f"**KEY:** `{record['api_key']}`\n\n"
        )
    await callback.message.edit_text(text, parse_mode="Markdown")

@router.callback_query(F.data == "apikey_delete")
async def apikey_delete_callback(callback: CallbackQuery, state: FSMContext):
    if not await check_access_callback(callback):
        return

    records = await DATABASE.api_key_print()
    if not records:
        await callback.message.edit_text('*Таблица api_key пуста*', reply_markup=kb.back_to_settings, parse_mode="Markdown")
        return

    text = ""
    for record in records:
        text += (
            f"**Client ID:** `{record['client']}`\n"
            f"**KEY:** `{record['api_key']}`\n\n"
        )
    await callback.message.edit_text(f'{text}\n*Введите client_id сервиса для удаления ключа:*', parse_mode="Markdown")
    await state.set_state(SetState.client_id)

@router.message(SetState.client_id)
async def apikey_delete_message(message: Message, state: FSMContext):
    client_id_for_delete = message.text.strip()
    records = await DATABASE.api_key_print()
    found = False
    for record in records:
        if record['client_id'] == client_id_for_delete:
            found = True
            break

    if not found:
        await message.answer('*Данного client_id не найдено*', parse_mode="Markdown")
    else:
        await DATABASE.delete_api_key(client_id_for_delete)
        await message.answer(
            f"*Ключ для сервиса `{client_id_for_delete}` удалён* ✅",
            reply_markup=kb.back_to_settings,
            parse_mode="Markdown"
        )
        await state.clear()