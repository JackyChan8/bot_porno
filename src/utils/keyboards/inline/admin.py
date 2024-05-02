from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def settings_prices_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='💫 Премиум', callback_data='premium_menu')]
        ]
    )


async def settings_premium_inline_keyboard(is_premium: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if is_premium:
        builder.row(
            InlineKeyboardButton(text='✏️ Изменить Премиум', callback_data='edit_premium_price')
        )
        builder.row(
            InlineKeyboardButton(text='👁 Показать Премиум', callback_data='show_premium_price')
        )
    else:
        builder.row(
            InlineKeyboardButton(text='➕ Добавить Премиум', callback_data='add_premium_price')
        )
    return builder.as_markup()


async def file_info_keyboard(file_id: int, type_file: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🗑 Удалить', callback_data=f'delete_file-{file_id}-{type_file}')]
        ],
        resize_keyboard=True,
    )


async def user_info_keyboard(user_id: int, is_ban: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if is_ban:
        builder.row(
            InlineKeyboardButton(text='⬆️ Разблокировать', callback_data=f'unblock_user-{user_id}')
        )
    else:
        builder.row(
            InlineKeyboardButton(text='⬇️ Заблокировать', callback_data=f'block_user-{user_id}')
        )
    return builder.as_markup()


async def settings_support_inline_keyboard(is_tech_support: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if is_tech_support:
        builder.row(
            InlineKeyboardButton(text='✏️ Изменить', callback_data='edit_tech_support')
        )
        builder.row(
            InlineKeyboardButton(text='👁 Показать', callback_data='show_tech_support')
        )
    else:
        builder.row(
            InlineKeyboardButton(text='➕ Добавить Тех.Поддержку', callback_data='add_tech_support')
        )
    return builder.as_markup()
