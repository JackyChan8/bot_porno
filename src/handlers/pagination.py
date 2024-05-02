from aiogram import Router
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import utils_func
from src.config import decorate_logging
from src.utils.pagination import pagination, Pagination

router = Router(name='pagination')


@router.callback_query(Pagination.filter())
@decorate_logging
async def pagination_handler(callback: CallbackQuery, callback_data: Pagination, session: AsyncSession) -> None:
    """Pagination Handler"""
    await utils_func.delete_before_message(callback)
    page: int = callback_data.page
    type_: str = callback_data.type

    await pagination(
        type_=type_,
        page=page,
        session=session,
        message=callback.message,
    )

