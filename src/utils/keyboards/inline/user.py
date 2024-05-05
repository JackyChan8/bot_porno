from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.config import settings


async def payments_choose_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='💳 Карты(🇷🇺 RUB | 🇺🇦 UAH | 🇰🇿 KZT', callback_data='premium_pay_cards')],
            [InlineKeyboardButton(text='💰 СБП | Скины | Крипта', callback_data='premium_pay_crypto')],
            [InlineKeyboardButton(text='🧑‍💻 Админ | RUB/UAH/BYN', callback_data='premium_pay_admin')],
            [InlineKeyboardButton(text='🤖 CryptoBot', callback_data='premium_pay_crypto-bot')],
        ]
    )


async def payments_actions_buttons_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Перейти к оплате 💸', url='https://google.com/')],
            [InlineKeyboardButton(text='Проверить оплату 🔍', callback_data='check_pay')],
            [InlineKeyboardButton(text='Отменить оплату ❌', callback_data='cancel_pay')],
        ]
    )


async def top_up_balance_buttons_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='50 RUB', callback_data='top-up-balance_50'),
                InlineKeyboardButton(text='100 RUB', callback_data='top-up-balance_100'),
            ],
            [
                InlineKeyboardButton(text='200 RUB', callback_data='top-up-balance_200'),
                InlineKeyboardButton(text='500 RUB', callback_data='top-up-balance_500'),
                InlineKeyboardButton(text='750 RUB', callback_data='top-up-balance_750'),
            ],
            [
                InlineKeyboardButton(text='1000 RUB', callback_data='top-up-balance_1000'),
            ]
        ]
    )


async def pass_verification_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Пройти проверку', url='https://t.me/dark_veref_bot'),
            ]
        ]
    )


async def subscribe_channels_buttons_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Подписаться 📢', url=settings.TELEGRAM_CHANNEL_URL)
            ],
            [InlineKeyboardButton(text='Выполнено ✅', callback_data='subscribe_success')],
        ]
    )
