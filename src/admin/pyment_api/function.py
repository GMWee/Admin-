from aiogram import Router
from aiogram.types import Message, CallbackQuery

import datetime

from src.base.database import DATABASE
from src.base.utils import get_user_subscription
from src.admin.user_settings import admin_settings_menu_keyboard as kb
from typing import Union


router = Router()

class pyment():



	async def set_credits(self, message: Message, credits):
		"""Смена кердитов"""
		from src.admin.user_settings.settings import ID_STORAGE
		await DATABASE.set_credits_info(ID_STORAGE.id, credits, 0)
		await message.answer(f"*Выданно {credits} кредитов*",reply_markup = kb.back_to_yoomoney , parse_mode="Markdown")



PYMENT = pyment()