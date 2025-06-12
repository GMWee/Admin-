from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Информация об аккаунте🌈', callback_data="settings"),
    ],
    [
        InlineKeyboardButton(text='Изменить настройки💎', callback_data="set_settigs"),
    ],
    [
        InlineKeyboardButton(text='BAN⏰', callback_data="ban"),
        InlineKeyboardButton(text='UnBUN🎟', callback_data="unban")
    ]
])


back_to_settings = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Главное меню🔑', callback_data="back_to_settings"),
    ]
])


settings = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Подписка🎁', callback_data="sub"),
        InlineKeyboardButton(text='Роль🎰', callback_data="role")
    ],
    [
        InlineKeyboardButton(text='Выдать кредиты💎', callback_data="credits"),
        InlineKeyboardButton(text='Пополнить баланс🔷', callback_data="balance")
    ],
    [
        InlineKeyboardButton(text='Главное меню🔑', callback_data="back_to_settings"),
    ]
])


sub_version = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='STANDARD', callback_data="sub_0")
    ],
    [
        InlineKeyboardButton(text='🟤 BRONZE', callback_data="sub_1")
    ],
    [
        InlineKeyboardButton(text='⚪️ SILVER', callback_data="sub_2")
    ],
    [
        InlineKeyboardButton(text='🟡 GOLD', callback_data="sub_3")
    ],
    [
        InlineKeyboardButton(text='🔷 PLATINUM', callback_data="sub_4")
    ],
    [
        InlineKeyboardButton(text='🏳️‍🌈👧🏿 ADMIN', callback_data="sub_5")
    ],
    [
        InlineKeyboardButton(text='Главное меню🔑', callback_data="back_to_settings")
    ]
])


role_2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Модератор', callback_data="Role_1")
    ],
    [
        InlineKeyboardButton(text='Пользователь', callback_data="Role_0")
    ],
    [
        InlineKeyboardButton(text='Главное меню🔑', callback_data="back_to_settings")
    ]
])


role_3 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Владелец', callback_data="Role_3")
    ],
    [
        InlineKeyboardButton(text='Админ', callback_data="Role_2")
    ],
    [
        InlineKeyboardButton(text='Модератор', callback_data="Role_1")
    ],
    [
        InlineKeyboardButton(text='Пользователь', callback_data="Role_0")
    ],
    [
        InlineKeyboardButton(text='Главное меню🔑', callback_data="back_to_settings")
    ]
])









