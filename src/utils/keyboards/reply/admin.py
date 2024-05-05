from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from .user import main_menu_button


async def start_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='👥 Пользователи')],
            [KeyboardButton(text='📢 Уведомления')],
            [KeyboardButton(text='🛠 Настройка')]
        ],
        resize_keyboard=True,
    )


async def notification_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='✉️ Отправить всем')],
            [main_menu_button],
        ],
        resize_keyboard=True,
    )


async def settings_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🌇 Фото'), KeyboardButton(text='🎥 Видео')],
            [KeyboardButton(text='🫰 Цены'), KeyboardButton(text='🛠 Тех.Поддержка')],
            [main_menu_button]
        ],
        resize_keyboard=True,
    )


async def file_reply_keyboard(type_file: str) -> ReplyKeyboardMarkup:
    def text_file(text_: str):
        return f'{text_} Фото' if type_file == 'фото' else f'{text_} Видео'

    add_text: str = text_file('Добавить')
    show_text: str = text_file('Показать')

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=add_text)],
            [KeyboardButton(text=show_text)],
            [main_menu_button]
        ],
        resize_keyboard=True,
    )
