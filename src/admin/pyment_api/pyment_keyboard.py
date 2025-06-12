from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Просмотреть таблицу🌈', callback_data="get_tabel")
    ],
    [
        InlineKeyboardButton(text='Добавить ключ🌈', callback_data="apikey_add")
    ],
    [
        InlineKeyboardButton(text='Удалить ключ💎', callback_data="apikey_delete")
    ]
])

back_to_settings = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Главное меню🔑', callback_data="back_to_yoomoney"),
    ]
])