from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.utils.filters import IsBanUser
from src.utils.text import user as user_text
from src.utils.text import admin as admin_text
from src.config import settings, decorate_logging
from src.utils.keyboards.reply import user as user_reply_keyboard
from src.utils.keyboards.reply import admin as admin_reply_keyboard

router = Router(name='cancel')


@router.message(IsBanUser(), F.text == 'Отмена ❌')
@decorate_logging
async def cancel_handler(message: Message, state: FSMContext) -> None:
    if message.from_user.id in settings.ADMINS_ID:
        buttons = await admin_reply_keyboard.start_reply_keyboard()
        text = admin_text.START_ADMIN_TEXT
    else:
        buttons = await user_reply_keyboard.start_reply_keyboard()
        text = user_text.START_USER_TEXT
    await state.clear()
    await message.answer(text, reply_markup=buttons)
