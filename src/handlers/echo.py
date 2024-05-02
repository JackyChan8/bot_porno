from aiogram.types import Message
from aiogram import Router

router = Router(name='echo')


@router.message()
async def echo_handler(message: Message):
    await message.answer(message.text)
