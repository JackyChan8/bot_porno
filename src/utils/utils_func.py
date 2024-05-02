import os

from aiogram.enums.parse_mode import ParseMode
from aiogram.types import CallbackQuery, Message, FSInputFile

from sqlalchemy.ext.asyncio import AsyncSession

from src.services import services
from src.config import decorate_logging
from src.utils.text import user as user_text
from src.utils.static_path import PHOTOS_PATH, VIDEO_PATH
from src.utils.keyboards.inline import user as user_inline_keyboard


PAYMENT_METHOD: dict[str, str] = {
    'cards': 'Карты',
    'crypto': 'СБП | Скины | Крипта',
    'admin': 'Админ',
    'crypto-bot': 'CryptoBot',
}


@decorate_logging
async def delete_before_message(action: Message | CallbackQuery) -> None:
    """Delete Before Message"""
    if isinstance(action, Message):
        await action.delete()
    else:
        await action.message.delete()


@decorate_logging
async def check_is_digit(text: str) -> bool:
    """Check Is Number and Positive"""
    return text.isdigit()


@decorate_logging
async def output_watch_file(file_name: str, type_file: str, message: Message, session: AsyncSession) -> None:
    """Output Watch File"""
    data = {
        'фото': (1, PHOTOS_PATH, ),
        'видео': (2, VIDEO_PATH, ),
    }

    user_id: int = message.from_user.id

    # Check Balance
    balance = await services.get_balance(user_id, session)
    if balance <= 1:
        buttons = await user_inline_keyboard.subscribe_channels_buttons_inline_keyboard()
        await message.answer(user_text.WATCH_FILE_NOT_BALANCE, reply_markup=buttons, parse_mode=ParseMode.HTML)
        return

    cost_watch, file_path = data.get(type_file)
    file: FSInputFile = FSInputFile(file_path + file_name)
    text: str = await user_text.watch_file_text(type_file)

    # Send File
    if type_file == 'фото':
        await message.bot.send_photo(
            photo=file,
            caption=text,
            parse_mode=ParseMode.HTML,
            chat_id=message.from_user.id,
        )
    else:
        await message.bot.send_video(
            video=file,
            caption=text,
            parse_mode=ParseMode.HTML,
            chat_id=message.from_user.id,
        )

    # Create Action
    await services.create_action(user_id, type_file, file_name, session)

    # Update Balance
    await services.update_balance(user_id, '-', cost_watch, session)


@decorate_logging
async def add_referral_link(user_id: int, referral_id: int, exist_user: bool, message: Message,
                            session: AsyncSession, earn_ref: int = 10) -> None:
    """Added Referral Link"""
    if referral_id == user_id:
        await message.answer(user_text.NOT_USE_SELF_REFERRAL_LINK)
    else:
        # Check Exists User
        if exist_user:
            return
        # Add To Database Referral Link
        result = await services.create_refer_link(user_id, referral_id, session)
        if result:
            # Add Money To Balance
            await services.update_balance(referral_id, '+', earn_ref, session)
            # Send Notification
            await message.bot.send_message(
                referral_id, user_text.SUCCESS_CREATE_BY_REFERRAL_LINK.format(username=message.from_user.username)
            )


@decorate_logging
async def get_files(message: Message) -> str:
    """Get Files From Message"""
    if message.photo:
        file_id: str = message.photo[-1].file_id
    else:
        obj_dict = message.dict()
        file_id: str = obj_dict[message.content_type]['file_id']
    return file_id


@decorate_logging
async def save_document(file_id: int, type_file: str, message: Message) -> str:
    """Save Document"""
    file = await message.bot.get_file(file_id)
    _, file_extension = os.path.splitext(file.file_path)
    file_name: str = message.date.now().strftime('%m_%d_%Y_%H_%M_%S') + f'_{file_id}' + file_extension

    if type_file == 'photo':
        destination = PHOTOS_PATH + file_name
    else:
        destination = VIDEO_PATH + file_name
    await message.bot.download(file=file_id, destination=destination)
    return file_name


@decorate_logging
async def get_files_name_download_file(message: Message, type_file: str, album: list[Message] = None) -> list[str]:
    """Get Files Names About Files"""
    files_names: list[str] = []
    # Check Group or Simple File
    if album:
        files_id: list[str] = []
        # Get Files ID
        for msg in album:
            file_id: str = await get_files(msg)
            files_id.append(file_id)
        # Save Files
        for file_id in files_id:
            path_file: str = await save_document(file_id, type_file, message)
            files_names.append(path_file)
    else:
        file_id: str = await get_files(message)
        path_file: str = await save_document(file_id, type_file, message)
        files_names.append(path_file)
    return files_names
