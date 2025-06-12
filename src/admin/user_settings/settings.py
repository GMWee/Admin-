from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command, CommandStart

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.base.config import CONFIG
from src.base.database import DATABASE
from src.admin.user_settings.function import SETTINGS
from src.admin.user_settings import admin_settings_menu_keyboard as kb

router = Router()


class settings_global_id:
	id = 0
	

ID_STORAGE = settings_global_id()


class SetState(StatesGroup):
	ID = State()
	CREDITS = State()
	BALANCE = State()
	
	
class Role:
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
		

class Menu:
	#меню "menu"
	def __init__(self):
		self.router = Router()
		self.setup_handlers()
	
	
	def setup_handlers(self):
		@self.router.message(Command('settings'))
		async def handle_settings_command(message: Message):
			if await ROLE.role_message(message) == False:
				await message.answer('*У вас нет доступа к данному боту! Так как вы не являетесь администрацией бота.*',
				                     parse_mode="Markdown")
				return
			await SETTINGS.open_menu(message)
		
		
		@self.router.callback_query(F.data == "settings")
		async def handle_settings_details_callback(callback: CallbackQuery):
			if await ROLE.role_callback(callback) == False:
				await callback.message.edit_text(
					'*У вас нет доступа к данному боту! Так как вы не являетесь администрацией бота.*',
					parse_mode="Markdown")
				return
			await SETTINGS.settings_chat(callback)
			await callback.answer()
		
		
		@self.router.callback_query(F.data == "back_to_settings")
		async def handle_back_to_settings_callback(callback: CallbackQuery):
			if await ROLE.role_callback(callback) == False:
				await callback.message.edit_text(
					'*У вас нет доступа к данному боту! Так как вы не являетесь администрацией бота.*',
					parse_mode="Markdown")
				return
			await SETTINGS.open_menu(callback)
			await callback.answer()
		
		
		@self.router.callback_query(F.data == "set_settigs")
		async def handle_settings_set_callback(callback: CallbackQuery):
			if await ROLE.role_callback(callback) == False:
				await callback.message.edit_text(
					'*У вас нет доступа к данному боту! Так как вы не являетесь администрацией бота.*',
					parse_mode="Markdown")
				return
			await SETTINGS.set_settings(callback)
			await callback.answer()
		
		
		@self.router.callback_query(F.data == "ban")
		async def handle_ban(callback: CallbackQuery):
			if await ROLE.role_callback(callback) == False:
				await callback.message.edit_text(
					'*У вас нет доступа к данному боту! Так как вы не являетесь администрацией бота.*',
					parse_mode="Markdown")
				return
			await SETTINGS.ban(ID_STORAGE.id, 1, callback)
			await callback.answer()
		
		
		@self.router.callback_query(F.data == "unban")
		async def handle_unban(callback: CallbackQuery):
			if await ROLE.role_callback(callback) == False:
				await callback.message.edit_text(
					'*У вас нет доступа к данному боту! Так как вы не являетесь администрацией бота.*',
					parse_mode="Markdown")
				return
			await SETTINGS.ban(ID_STORAGE.id, 0, callback)
			await callback.answer()


class UserSettings:
	#меню "Изменить настройки💎"
	def __init__(self):
		self.router = Router()
		self.setup_hendle()
		
		
	def setup_hendle(self):
		@self.router.callback_query(F.data == "sub")
		async def handle_settings_sub_callback(callback: CallbackQuery):
			if await ROLE.role_callback(callback) == False:
				await callback.message.edit_text('*У вас нед доступа к данному боту! Так как вы не являетесь администрацией бота.*', parse_mode = "Markdown")
				return
			await SETTINGS.set_sub(callback)
			await callback.answer()
		
		
		@self.router.callback_query(F.data.startswith('sub_'))
		async def set_sub(callback: CallbackQuery):
			data = int(callback.data.split("_")[1])
		
			if await ROLE.role_callback(callback) == False:
				await callback.message.edit_text('*У вас нед доступа к данному боту! Так как вы не являетесь администрацией бота.*', parse_mode = "Markdown")
				return
			await SETTINGS.sub_update(ID_STORAGE.id, data)
			await callback.message.edit_text('*Подписка изменена✅*',reply_markup=kb.back_to_settings, parse_mode="Markdown")
			await callback.answer()
		
		
		@self.router.callback_query(F.data == "role")
		async def role(callback: CallbackQuery):
			if await ROLE.role_callback(callback) == False:
				await callback.message.edit_text('*У вас нед доступа к данному боту! Так как вы не являетесь администрацией бота.*', parse_mode = "Markdown")
				return
			await SETTINGS.user_role(callback)
			await callback.answer()
		
		
		@self.router.callback_query(F.data.startswith("Role_"))
		async def role(callback: CallbackQuery):
			role = int(callback.data.split("_")[1])
			if await ROLE.role_callback(callback) == False:
				await callback.message.edit_text('*У вас нед доступа к данному боту! Так как вы не являетесь администрацией бота.*', parse_mode = "Markdown")
				return
			await SETTINGS.set_role(callback, role)
			await callback.answer()
		
		
		@self.router.callback_query(F.data == 'credits')
		async def setid_cmd(callback: CallbackQuery, state: FSMContext):
		    if not await ROLE.role_message(callback):
		        await callback.message.edit_text('*У вас нет доступа к данной команде! Так как вы не являетесь администрацией бота.*', parse_mode="Markdown")
		        return
		    await callback.message.answer('<b>Введите кол-во кредитов для пользователя:</b>', parse_mode='HTML')
		    await state.set_state(SetState.CREDITS)
		
		
		@self.router.message(SetState.CREDITS)
		async def process_set_id(message: Message, state: FSMContext):
			user_id_to_set = int(message.text)
			await SETTINGS.set_credits(message, user_id_to_set)
			await state.clear()
			
		@self.router.callback_query(F.data == "balance")
		async def up_balance(callback: CallbackQuery, state: FSMContext):
			if not await ROLE.role_message(callback):
				await callback.message.edit_text(
					'*У вас нет доступа к данной команде! Так как вы не являетесь администрацией бота.*',
					parse_mode="Markdown")
				return
			await callback.message.answer('<b>Введите кол-во средств для пользователя:</b>', parse_mode='HTML')
			await state.set_state(SetState.BALANCE)
			
			
		@self.router.message(SetState.BALANCE)
		async def process_up_balance(message: Message, state: FSMContext):
			data = int(message.text)
			await SETTINGS.set_balance(message, data)
			await state.clear()
			
			
			
#смена id для смены настроек пользователя в чате
@router.message(Command('setid'))
async def setid_cmd(message: Message, state: FSMContext):
    if not await SETTINGS.role_message(message):
        await message.answer('*У вас нет доступа к данной команде! Так как вы не являетесь администрацией бота.*', parse_mode="Markdown")
        return
    await message.answer('<b>Введите ID пользователя</b>', parse_mode='HTML')
    await state.set_state(SetState.ID)


@router.message(SetState.ID)
async def process_set_id(message: Message, state: FSMContext):
	try:
		user_id_to_set = int(message.text)
		if not await DATABASE.get_or_create_user(user_id_to_set, False):
			await message.answer('<b><em>Ошибка</em> ID чата не найден... Повторите попытку❌</b>', parse_mode='HTML')
		else:
			ID_STORAGE.id = user_id_to_set
			await message.reply(f'<b>Чат</b> <em>{user_id_to_set}</em> <b>найден и установлен✅</b>', parse_mode='HTML')
			await state.clear()
	except ValueError:
		await message.answer('<b><em>Ошибка...</em> Введите корректный числовой ID. Повторите попытку❌</b>',
							 parse_mode='HTML')

	
MENU = Menu()
USERSETTINGS = UserSettings()
ROLE = Role()