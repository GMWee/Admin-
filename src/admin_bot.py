import aiogram
import aiohttp
import asyncio

from src.base.config import CONFIG
from src.admin.user_settings import settings
from src.admin.user_settings.settings import MENU, USERSETTINGS
from src.admin.pyment_api import pyment
from src.base.database import DATABASE


class Bot:
	def __init__(self):
		self.bot: aiogram.Bot = ...
		self.dispatch = None
		self._shutdown_event = asyncio.Event()


	async def run(self):
		await DATABASE.open_connection(
			CONFIG["database_host"],
			CONFIG["database_port"],
			CONFIG["database_user"],
			CONFIG["database_password"],
			CONFIG["database_database"],
		)

		self.bot = aiogram.Bot(CONFIG["admin_token"])
		dispatch = aiogram.Dispatcher()

		await self._set_commands()

		dispatch.include_router(MENU.router)
		dispatch.include_router(USERSETTINGS.router)
		dispatch.include_router(settings.router)
		dispatch.include_router(pyment.router)

		async with aiohttp.ClientSession() as session:
			try:
				await dispatch.start_polling(self.bot, skip_updates=True, aiohttp_session=session)
			finally:
				await self.bot.session.close()
				await DATABASE.close_connection()

	async def _set_commands(self):
		commands = [
			aiogram.types.BotCommand(command="setid", description="Изменить id чата"),
			aiogram.types.BotCommand(command="yoomoney", description="Сменить ключ YooMoney"),
			aiogram.types.BotCommand(command="settings", description="Настройки чата"),
			aiogram.types.BotCommand(command="donate", description="Меню донатов")

		]
		await self.bot.set_my_commands(commands)
