from aiogram import Router
from aiogram.types import Message, CallbackQuery

import datetime

from src.base.database import DATABASE
from src.base.utils import get_user_subscription
from src.admin.user_settings import admin_settings_menu_keyboard as kb
from typing import Union


router = Router()

class Settings:
	"""Проверка роли"""
	async def role_message(self, message: Message):
		user_id = message.from_user.id
		user = await DATABASE.get_or_create_user(user_id, False)
		if user[3] < 1:
			return False
		else:
			return True

	async def role_callback(self, callback: CallbackQuery):
		user_id = callback.from_user.id
		user = await DATABASE.get_or_create_user(user_id, False)
		if user[3] < 1:
			return False
		else:
			return True


	"""Основная система меню"""
	async def open_menu(self, context: Union[Message, CallbackQuery]):
		"""Главное меню"""
		text = '*User menu settings:*'
		if isinstance(context, Message):
			await context.answer(text, reply_markup=kb.menu, parse_mode="Markdown")
		elif isinstance(context, CallbackQuery):
			if context.message:
				try:
					await context.message.edit_text(text, reply_markup=kb.menu, parse_mode="Markdown")
				except Exception as e:
					print(f"Error editing message: {e}")
					await context.message.answer(text, reply_markup=kb.menu, parse_mode="Markdown")
			await context.answer()


	async def settings_chat(self, callback: CallbackQuery):
		from src.admin.user_settings.settings import ID_STORAGE
		"""Информация об аккаунте"""
		user_id = ID_STORAGE.id
		if user_id == 0:
			await callback.message.edit_text("ID пользователя не установлен. Используйте команду /setid.",
											 parse_mode="Markdown")
			await callback.answer()
			return

		user = await DATABASE.get_or_create_user(user_id)
		if not user:
			await callback.message.edit_text(f"Пользователь с ID '{user_id}' не найден.", parse_mode="Markdown")
			await callback.answer()
			return

		sub = get_user_subscription(user)
		sub_info = await DATABASE.get_subscription(sub)
		sub_models = await DATABASE.get_subscription_models(sub)
		current_model = await DATABASE.get_model(user[4])
		cred = user[5]

		text = f"*❗️ Информация о пользователе '{ID_STORAGE.id}'*\n\n"
		text += f"— *Подписка*: {sub_info[1]}\n"
		text += f"— *Выбранная модель*: {current_model[1]}\n"
		text += f"— *Баланс:* {user[11]}⭐️\n"
		text += f"— *Кредиты*: _{cred}💎 / {sub_info[2]}💎_\n"
		if sub_info[4] == 0:
			text += f"— *Фото недоступны*\n\n"
		else:
			text += f"— *Стоимость фото*: _{sub_info[4]}💎_\n\n"

		text += f"— *Admin‼️\n*" if user[3] >= 1 else "— *User*\n"
		text += "🤖 Доступные модели:\n"

		for mod_tuple in sub_models:
			model = await DATABASE.get_model(mod_tuple[0])
			text += f"— {model[1]}\n"

		await callback.message.edit_text(text, reply_markup=kb.back_to_settings, parse_mode="Markdown")
		await callback.answer()


	async def set_settings(self, callback: CallbackQuery):
		"""Выбор настройки для изменения"""
		await callback.message.edit_reply_markup(reply_markup=kb.settings, parse_mode="Markdown")
		await callback.answer()


	async def set_sub(self, callback: CallbackQuery):
		"""Смена подписки"""
		await callback.message.edit_reply_markup(reply_markup=kb.sub_version, parse_mode="Markdown")
		await callback.answer()


	async def sub_update(self, telegram_id: int, sub_id: int):
		"""Выдача подписки"""
		dt = datetime.datetime.now() + datetime.timedelta(days=28)
		await DATABASE.set_user_subscription(telegram_id, sub_id, dt.timestamp())
		si = await DATABASE.get_subscription(sub_id)
		await DATABASE.set_credits_info(telegram_id, si[2], 0)

	async def ban(self, telegram_id: int, num: int, callback: CallbackQuery):
		"""Выдать бан/разбан"""
		await DATABASE.set_ban(num, telegram_id)
		text = '*Аккаунт забаннен*✅' if num == 1 else '*Аккаунт разбаннен*✅'
		await callback.message.edit_text(text, reply_markup=kb.back_to_settings, parse_mode="Markdown")
		await callback.answer()

	async def user_role(self, callback: CallbackQuery):
		"""Меню ролей в зависимости от уровня админа"""
		from src.admin.user_settings.settings import ID_STORAGE
		admin_id = callback.from_user.id
		role_admin = await DATABASE.get_or_create_user(admin_id, False)
		print(role_admin)
		role_user = await DATABASE.get_or_create_user(ID_STORAGE.id, False)
		if role_admin[3] == 1:
			await callback.message.edit_text('*Ваш ранг слишком низкий❗️\n У вас нет доступа к этой функции❗️*',
											 reply_markup=kb.back_to_settings, parse_mode="Markdown")
		elif role_admin[3] == 2:
			await callback.message.edit_text('*Set role from user*',
											 reply_markup=kb.role_2, parse_mode="Markdown")
		elif role_admin[3] == 3:
			await callback.message.edit_text('*Set role from user*',
											 reply_markup=kb.role_3, parse_mode="Markdown")


	async def set_role(self, callback: CallbackQuery, role: int):
		"""Сменить роль пользователя"""
		from src.admin.user_settings.settings import ID_STORAGE
		admin_id = callback.message.from_user.id
		role_admin = await DATABASE.get_or_create_user(admin_id, False)
		role_user = await DATABASE.get_or_create_user(ID_STORAGE.id, False)
		if role_admin[3] <= role_user[3]:
			await callback.message.edit_text("*Вы не можете изменить роль данного пользователя❗️\nТ.к ваш ранг ниже или идентичен❗️*✅",
											 reply_markup=kb.back_to_settings,parse_mode="Markdown")
		await DATABASE.set_role(role ,ID_STORAGE.id)
		await callback.message.edit_text("*Роль изменена*✅", reply_markup=kb.back_to_settings, parse_mode="Markdown")
		await callback.answer()

	async def set_credits(self, message: Message, credits):
		"""Смена кердитов"""
		from src.admin.user_settings.settings import ID_STORAGE
		await DATABASE.set_credits_info(ID_STORAGE.id, credits, 0)
		await message.answer(f"*Выданно {credits} кредитов*",reply_markup = kb.back_to_settings , parse_mode="Markdown")
		
	async def set_balance(self, message: Message, sum):
		"""Смена значения баланса"""
		from src.admin.user_settings.settings import ID_STORAGE
		await DATABASE.set_user_balance(ID_STORAGE.id, sum)
		await message.answer(f"*Выданно {sum} звезд*",reply_markup = kb.back_to_settings , parse_mode="Markdown")

SETTINGS = Settings()