import asyncio
from typing import Any

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message, CallbackQuery, ContentType, ReplyKeyboardRemove, FSInputFile

from sqlalchemy.ext.asyncio import AsyncSession

from src.services import services
from src.utils.filters import IsAdmin
from src.config import decorate_logging
from src.utils.pagination import pagination
from src.utils.text import user as user_text
from src.utils.text import admin as admin_text
from src.utils.states import admin as admin_state
from src.utils.static_path import VIDEO_PATH, PHOTOS_PATH
from src.utils.keyboards.reply.user import cancel_reply_command
from src.utils.keyboards.reply import admin as admin_reply_keyboard
from src.utils.keyboards.inline import admin as admin_inline_keyboard
from src.utils.utils_func import check_is_digit, get_files_name_download_file, delete_before_message, send_notification

router = Router(name='admin')


@router.message(IsAdmin(), F.text == '🔝 Главное Меню')
@router.message(IsAdmin(), Command('start'))
@decorate_logging
async def admin_start_command(message: Message) -> None:
    """Start Command"""
    buttons = await admin_reply_keyboard.start_reply_keyboard()
    await message.answer(admin_text.START_ADMIN_TEXT, reply_markup=buttons)


@router.callback_query(IsAdmin(), F.data == 'main_menu')
@decorate_logging
async def admin_start_inline_command(callback: CallbackQuery) -> None:
    """Start Inline"""
    await admin_start_command(callback.message)


# ==================== Prices
@router.message(IsAdmin(), F.text == '👥 Пользователи')
@decorate_logging
async def admin_users_command(message: Message, session: AsyncSession) -> None:
    """Show Users Pagination"""
    count_users: int = await services.get_count_users(session=session)
    if count_users:
        await delete_before_message(message)
        await pagination(
            type_='пользователи',
            message=message,
            session=session,
        )
    else:
        await message.answer(admin_text.NOT_EXIST_USERS_TEXT)


@router.callback_query(IsAdmin(), F.data.startswith('пользователи_№'))
@decorate_logging
async def admin_user_show(callback: CallbackQuery, session: AsyncSession) -> None:
    """Show User Information"""
    data: list[str] = callback.data.split('_№')
    user_id: int = int(data[-1])
    # Get User
    _, is_ban, cnt_photos, cnt_videos, is_premium, balance = await services.get_info_user(user_id, session)
    # Output Information
    text = await user_text.profile_user_text(user_id, cnt_photos, cnt_videos, is_premium, balance, is_admin=True)
    buttons = await admin_inline_keyboard.user_info_keyboard(user_id, is_ban)
    await callback.message.answer(text, reply_markup=buttons, parse_mode=ParseMode.HTML)


@router.callback_query(IsAdmin(), F.data.startswith('block_user'))
@decorate_logging
async def admin_user_block(callback: CallbackQuery, session: AsyncSession) -> None:
    """Block User Information"""
    data: list[str] = callback.data.split('-')
    user_id: int = int(data[-1])
    # Block User
    await services.blocking_user(user_id, True, callback.message, session)


@router.callback_query(IsAdmin(), F.data.startswith('unblock_user'))
@decorate_logging
async def admin_user_un_block(callback: CallbackQuery, session: AsyncSession) -> None:
    """UnBlock User Information"""
    data: list[str] = callback.data.split('-')
    user_id: int = int(data[-1])
    # Block User
    await services.blocking_user(user_id, False, callback.message, session)


# ==================== Notification
@router.message(IsAdmin(), F.text == '📢 Уведомления')
@decorate_logging
async def admin_notify_command(message: Message) -> None:
    """Notification Command"""
    buttons = await admin_reply_keyboard.notification_reply_keyboard()
    await message.answer(admin_text.CHOOSE_COMMAND, reply_markup=buttons, parse_mode=ParseMode.HTML)


@router.message(IsAdmin(), F.text == '✉️ Отправить всем')
@decorate_logging
async def admin_send_all_notify_command(message: Message, state: FSMContext) -> None:
    """Notification Send Command"""
    # Setup State
    await state.set_state(admin_state.NotificationState.message)

    buttons = await cancel_reply_command()
    await message.answer(admin_text.WRITE_MESSAGE_NOTIFY, reply_markup=buttons, parse_mode=ParseMode.HTML)


@router.message(IsAdmin(), admin_state.NotificationState.message, F.text != 'Отмена ❌')
@decorate_logging
async def admin_notification_sending(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """Notication Send to Users"""
    if not message.text:
        await message.answer(admin_text.WRITE_MESSAGE_NOTIFY, parse_mode=ParseMode.HTML)
        return

    from sqlalchemy import null

    # Clear State
    await state.clear()

    # Get users
    users = await services.get_users(session=session, offset=null(), limit=null())

    # Send Admin Notification Success Sending
    await message.answer(admin_text.NOTIFY_SUCCESS_SEND, parse_mode=ParseMode.HTML)
    await admin_start_command(message)

    # Send Notification
    tasks = [send_notification(message.bot, user, message.text) for user in users]
    await asyncio.gather(*tasks)


# ==================== Settings
@router.message(IsAdmin(), F.text == '🛠 Настройка')
@decorate_logging
async def admin_settings_command(message: Message) -> None:
    """Settings Command"""
    buttons = await admin_reply_keyboard.settings_reply_keyboard()
    await message.answer(admin_text.CHOOSE_COMMAND, reply_markup=buttons, parse_mode=ParseMode.HTML)


# =================== Files
@router.message(IsAdmin(), F.text.in_({'🌇 Фото', '🎥 Видео'}))
@decorate_logging
async def admin_files_command(message: Message) -> None:
    """Files Command"""
    type_file: str = message.text.split(' ')[-1].lower()

    buttons = await admin_reply_keyboard.file_reply_keyboard(type_file)
    await message.answer(admin_text.CHOOSE_COMMAND, reply_markup=buttons, parse_mode=ParseMode.HTML)


@router.message(IsAdmin(), F.text.in_({'Добавить Фото', 'Добавить Видео'}))
@decorate_logging
async def admin_add_files_command(message: Message, state: FSMContext) -> None:
    """Add Files Command"""
    type_file: str = 'photo' if message.text.split(' ')[-1].lower() == 'фото' else 'video'
    await state.set_state(admin_state.FileState.files)
    await state.update_data(type_file=type_file)

    button_cancel = await cancel_reply_command()
    text: str = await admin_text.add_file_text(type_file)
    await message.answer(text, reply_markup=button_cancel, parse_mode=ParseMode.HTML)


@router.message(IsAdmin(),
                F.content_type.in_([ContentType.PHOTO, ContentType.DOCUMENT, ContentType.VIDEO]),
                admin_state.FileState.files)
@decorate_logging
async def admin_add_files(message: Message, state: FSMContext,
                          session: AsyncSession, album: list[Message] = None) -> None:
    """Add Files"""
    # Get Data
    data: dict = await state.get_data()
    type_file: str = data.get('type_file')
    # Clear State
    await state.clear()
    await message.answer(admin_text.PLEASE_WAIT, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    # Get Files Name
    files_name: list[str] = await get_files_name_download_file(message, type_file, album)
    # Create Files
    is_created: bool = await services.create_file(files_name, type_file, session, message)
    if is_created:
        await admin_start_command(message)


@router.message(IsAdmin(), F.text.in_({'Показать Фото', 'Показать Видео'}))
@decorate_logging
async def admin_show_files_command(message: Message, session: AsyncSession) -> None:
    """Show Files Pagination"""
    type_file: str = message.text.split(' ')[-1].lower()
    count_files: int = await services.get_count_files(type_file, session)
    if count_files:
        await delete_before_message(message)
        await pagination(
            type_=type_file,
            message=message,
            session=session,
        )
    else:
        await message.answer(admin_text.NOT_EXIST_FILES_TEXT, parse_mode=ParseMode.HTML)


@router.callback_query(IsAdmin(), F.data.startswith('фото_№') | F.data.startswith('видео_№'))
@decorate_logging
async def admin_file_show(callback: CallbackQuery, session: AsyncSession) -> None:
    """Show File Information"""
    user_id: int = callback.from_user.id
    data: list[str] = callback.data.split('_№')
    type_file: str = data[0]
    file_id: int = int(data[-1])
    file_path: str = PHOTOS_PATH if type_file == 'фото' else VIDEO_PATH
    # Get File Info
    file_name, created_at = await services.get_file_by_id(file_id, type_file, session)
    # Output File With Button
    buttons = await admin_inline_keyboard.file_info_keyboard(file_id, type_file)
    file: FSInputFile = FSInputFile(file_path + file_name)
    if type_file == 'фото':
        await callback.bot.send_photo(
            chat_id=user_id,
            photo=file,
            reply_markup=buttons,
        )
    else:
        await callback.bot.send_video(
            chat_id=user_id,
            video=file,
            reply_markup=buttons,
        )


@router.callback_query(IsAdmin(), F.data.startswith('delete_file'))
@decorate_logging
async def admin_file_delete(callback: CallbackQuery, session: AsyncSession) -> None:
    """Delete File"""
    data: list[str] = callback.data.split('-')
    file_id: int = int(data[1])
    type_file: str = data[2]
    await services.delete_file(file_id, type_file, session, callback.message)


# ==================== Prices
@router.message(IsAdmin(), F.text == '🫰 Цены')
@decorate_logging
async def admin_settings_prices_command(message: Message, session: AsyncSession) -> None:
    """Prices Command"""
    buttons = await admin_inline_keyboard.settings_prices_inline_keyboard()
    await message.answer(admin_text.CHOOSE_COMMAND, reply_markup=buttons)


@router.callback_query(IsAdmin(), F.data == 'premium_menu')
@decorate_logging
async def admin_premium_menu_command(callback: CallbackQuery, session: AsyncSession) -> None:
    """Premium Menu Command"""
    # Check Premium Prices Exists
    is_premium: bool = await services.check_exist_premium_price(session)
    buttons = await admin_inline_keyboard.settings_premium_inline_keyboard(is_premium)
    await callback.message.answer(admin_text.CHOOSE_COMMAND, reply_markup=buttons)


@router.callback_query(IsAdmin(), F.data.in_({'add_premium_price', 'edit_premium_price'}))
@decorate_logging
async def admin_add_premium_price(callback: CallbackQuery, state: FSMContext) -> None:
    """Add / Edit Price"""
    action: str = callback.data.split('_')[0]
    # Set State
    await state.set_state(admin_state.PriceState.price)
    await state.update_data(action=action)
    button_cancel = await cancel_reply_command()
    await callback.message.answer(admin_text.WRITE_PRICE, reply_markup=button_cancel, parse_mode=ParseMode.HTML)


@router.message(IsAdmin(), admin_state.PriceState.price, F.text != 'Отмена ❌')
@decorate_logging
async def admin_add_premium_price_save(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """Add Premium Price"""
    text: dict[str, Any] = admin_text.WRITE_PRICE_INCORRECT_SUM.as_kwargs()
    # Check Is Number and Positive
    if not message.text or not await check_is_digit(message.text):
        await message.answer(**text)
        return
    try:
        data: dict = await state.get_data()
        await state.clear()
        price: int = int(message.text)

        if data.get('action') == 'add':
            # Add Price
            is_created: bool = await services.create_premium_price(price, message, session)
        else:
            # Update Price
            is_created: bool = await services.update_premium_price(price, message, session)

        if is_created:
            await admin_start_command(message)
    except Exception as exc:
        await message.answer(**text)


@router.callback_query(IsAdmin(), F.data == 'show_premium_price')
@decorate_logging
async def show_premium_price(callback: CallbackQuery, session: AsyncSession) -> None:
    """Show Premium Price Service"""
    premium_price: int = await services.get_premium_price(session)
    await callback.message.answer(admin_text.SHOW_PRICE.format(price=premium_price))


# ==================== Tech Support
@router.message(IsAdmin(), F.text == '🛠 Тех.Поддержка')
@decorate_logging
async def admin_tech_support_command(message: Message, session: AsyncSession) -> None:
    """Tech Support Menu Command"""
    # Check Tech Support Exists
    is_tech_support: bool = await services.check_exist_tech_support(session)
    buttons = await admin_inline_keyboard.settings_support_inline_keyboard(is_tech_support)
    await message.answer(admin_text.CHOOSE_COMMAND, reply_markup=buttons)


@router.callback_query(IsAdmin(), F.data.in_({'add_tech_support', 'edit_tech_support'}))
@decorate_logging
async def admin_add_tech_support(callback: CallbackQuery, state: FSMContext) -> None:
    """Add / Edit Tech Support Command"""
    action: str = callback.data.split('_')[0]
    # Set State
    await state.set_state(admin_state.TechSupportState.username)
    await state.update_data(action=action)
    button_cancel = await cancel_reply_command()
    await callback.message.answer(admin_text.WRITE_USERNAME_SUPPORT, reply_markup=button_cancel, parse_mode=ParseMode.HTML)


@router.message(IsAdmin(), admin_state.TechSupportState.username, F.text != 'Отмена ❌')
@decorate_logging
async def admin_add_tech_support_save(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """Add / Edit Tech Support Save"""
    if not message.text:
        await message.answer(**admin_text.WRITE_USERNAME_INCORRECT.as_kwargs())
        return

    data: dict = await state.get_data()
    await state.clear()

    if data.get('action') == 'add':
        # Add Tech Suppoer
        is_created: bool = await services.create_tech_support(message.text, message, session)
    else:
        # Edit Tech Support
        is_created: bool = await services.update_tech_support(message.text, message, session)

    if is_created:
        await admin_start_command(message)


@router.callback_query(IsAdmin(), F.data == 'show_tech_support')
@decorate_logging
async def show_tech_support(callback: CallbackQuery, session: AsyncSession) -> None:
    """Show Tech Support Service"""
    tech_support: str = await services.get_tech_support(session)
    await callback.message.answer(admin_text.SHOW_TECH_SUPPORT.format(username=tech_support), parse_mode=ParseMode.HTML)
