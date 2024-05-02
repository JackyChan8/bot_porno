from aiogram.types import Message
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from src.services import services
from src.config import decorate_logging


paginationTypeText: dict = {
    'пользователи': ('Пользователи', services.get_count_users, services.get_users),
    'фото': ('Фото', services.get_count_files, services.get_files),
    'видео': ('Видео', services.get_count_files, services.get_files),
}


class Pagination(CallbackData, prefix="pag"):
    action: str  # Действие
    page: int  # Номер страницы
    type: str  # Тип Пагинации


@decorate_logging
async def pagination(type_: str, message: Message, session: AsyncSession, page: int = 0) -> None:
    builder = InlineKeyboardBuilder()
    limit: int = 3
    start_offset: int = page * 3
    end_offset: int = start_offset + limit

    pagination_type = paginationTypeText.get(type_)

    # Get Data
    data = await pagination_type[2](type_, session=session, offset=start_offset)
    count = await pagination_type[1](type_, session=session)

    for data_id in data:
        if type_ == 'пользователи':
            author = await message.bot.get_chat_member(data_id, data_id)
            button_text = author.user.username
        else:
            button_text = f'{pagination_type[0]} №{data_id}'

        builder.row(
            InlineKeyboardButton(text=button_text, callback_data=f'{type_}_№{data_id}')
        )

    buttons_row: list = []
    if page > 0:  # Проверка, что страница не первая
        buttons_row.append(InlineKeyboardButton(
            text="⬅️",
            callback_data=Pagination(
                action="prev",
                page=page - 1,
                type=type_,
            ).pack()
        ))

    if end_offset < count:  # Проверка, что ещё есть пользователи для следующей страницы
        buttons_row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=Pagination(
                    action="next",
                    page=page + 1,
                    type=type_,
                ).pack()
            ))

    builder.row(*buttons_row)
    builder.row(InlineKeyboardButton(text='« Назад', callback_data='main_menu'))

    # Output Message
    message_text = f'Ваши {pagination_type[0]}'
    await message.answer(
        message_text,
        reply_markup=builder.as_markup()
    )
