from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu_button = KeyboardButton(text='🔝 Главное Меню')


async def start_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Смотреть Фото 🌇'), KeyboardButton(text='Смотреть Видео 🎥')],
            [KeyboardButton(text='Профиль 👤'), KeyboardButton(text='Заработать 💎')],
            [KeyboardButton(text='Premium-Подписка 🌟'), KeyboardButton(text='Категории 🔥')],
        ],
        resize_keyboard=True,
    )


async def profile_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Пополнить 💎'), KeyboardButton(text='Вывести 💳')],
            [main_menu_button],
        ],
        resize_keyboard=True,
    )


async def earn_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='➕ Предложить материал')],
            [KeyboardButton(text='Пригласить друга 👥'), KeyboardButton(text='Получить бонус 🎁')],
            [main_menu_button],
        ],
        resize_keyboard=True,
    )


async def premium_subscribe_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='💫 Купить Premium-подписку')],
            [main_menu_button],
        ],
        resize_keyboard=True,
    )


async def cancel_reply_command() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Отмена ❌')],
        ],
        resize_keyboard=True,
    )


async def categories_reply_command() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [main_menu_button],
        ],
        resize_keyboard=True,
    )
