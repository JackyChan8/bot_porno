from typing import Any

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject

from sqlalchemy.ext.asyncio import AsyncSession

from src.services import services
from src.utils.text import user as user_text
from src.utils.states import user as user_state
from src.utils.filters import IsAdmin, IsBanUser
from src.utils.keyboards.reply import user as user_reply_keyboard
from src.utils.keyboards.inline import user as user_inline_keyboard
from src.utils.utils_func import (check_is_digit, delete_before_message, output_watch_file,
                                  add_referral_link, PAYMENT_METHOD)

from src.config import settings, decorate_logging


router = Router(name='users')


@router.message(~IsAdmin(), IsBanUser(), F.text.in_({'🔝 Главное Меню'}))
@router.message(~IsAdmin(), IsBanUser(), Command('start'))
@decorate_logging
async def user_start_command(message: Message, session: AsyncSession, command: CommandObject = None) -> None:
    """Start Command Reply"""
    user_id: int = message.from_user.id
    args: str | None = command.args if command else None

    # Check Exist User
    exist_user: bool = await services.check_exist_user(user_id, session)
    if not exist_user:
        # Create User
        await services.create_user(user_id, session)

    # Added Referral Link
    if args and args.isdigit():
        await add_referral_link(user_id, int(args), exist_user, message, session)

    buttons = await user_reply_keyboard.start_reply_keyboard()
    await message.answer(user_text.START_USER_TEXT, reply_markup=buttons, parse_mode=ParseMode.HTML)


# ==================== Watch File
@router.message(~IsAdmin(), IsBanUser(), F.text.in_({'Смотреть Фото 🌇', 'Смотреть Видео 🎥'}))
@decorate_logging
async def user_watch_file(message: Message, session: AsyncSession) -> None:
    """Watch File Command Reply"""
    type_file: str = message.text.split(' ')[1].lower()

    # Get Filename
    filename: str | None = await services.get_random_file(message.from_user.id, type_file, session)
    if not filename:
        await message.answer(user_text.WATCH_FILE_NOT_EXIST_FILE)
        return

    # Output Info File
    await output_watch_file(filename, type_file, message, session)


# ==================== Profile
@router.message(~IsAdmin(), IsBanUser(), F.text == 'Профиль 👤')
@decorate_logging
async def user_profile_command(message: Message, session: AsyncSession) -> None:
    """Profile Command Reply"""
    user_id: int = message.from_user.id
    # Get Profile Information
    _, is_ban, cnt_photos, cnt_videos, is_premium, balance = await services.get_info_user(user_id, session)
    # Get Tech Support
    tech_support = await services.get_tech_support(session)

    buttons = await user_reply_keyboard.profile_reply_keyboard()
    text = await user_text.profile_user_text(
        user_id, cnt_photos, cnt_videos, is_premium, balance, admin_username=tech_support
    )
    await message.answer(text, reply_markup=buttons, parse_mode=ParseMode.HTML)


@router.message(~IsAdmin(), IsBanUser(), F.text == 'Пополнить 💎')
@decorate_logging
async def user_top_up_command(message: Message) -> None:
    """Profile Top Up Balance Command Reply"""
    buttons = await user_inline_keyboard.top_up_balance_buttons_inline_keyboard()
    await message.answer(
        user_text.PROFILE_TOP_UP_TEXT,
        reply_markup=buttons,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(~IsAdmin(), IsBanUser(), F.data.startswith('top-up-balance'))
@decorate_logging
async def user_top_up_buy_step_1(callback: CallbackQuery, state: FSMContext) -> None:
    """Buy Premium Step 1 Subscribe Command Reply"""
    sum_pay: int = int(callback.data.split('_')[-1])
    # Set State Transaction
    await state.set_state(user_state.TransactionPay.pay_method)
    await state.update_data(type_pay='Баланс', sum=sum_pay)
    # Choose Payment Method
    buttons = await user_inline_keyboard.payments_choose_inline_keyboard()
    await callback.message.answer(**user_text.CHOOSE_PAYMENT_TEXT.as_kwargs(), reply_markup=buttons)


@router.message(~IsAdmin(), IsBanUser(), F.text == 'Вывести 💳')
@decorate_logging
async def user_profile_out_balance_command(message: Message, state: FSMContext) -> None:
    """Profile Output Command Reply"""
    await state.set_state(user_state.OutBalanceStates.sum)

    buttons = await user_reply_keyboard.cancel_reply_command()
    await message.answer(**user_text.PROFILE_OUT_BALANCE.as_kwargs(), reply_markup=buttons)


@router.message(~IsAdmin(), IsBanUser(), user_state.OutBalanceStates.sum, F.text != 'Отмена ❌')
@decorate_logging
async def user_profile_out_balance_message(message: Message) -> None:
    """Profile Output Balance Message"""
    text: dict[str, Any] = user_text.PROFILE_OUT_BALANCE_INCORRECT_SUM.as_kwargs()
    try:
        # Check Is Number and Positive
        if not await check_is_digit(message.text):
            await message.answer(**text)
            return

        balance = 5

        # Check Is Number More Balance
        if int(message.text) <= balance:
            await message.answer(**user_text.PROFILE_OUT_BALANCE_LESS.as_kwargs())
        else:
            await message.answer(**user_text.PROFILE_OUT_BALANCE_DONT_ENOUGH.as_kwargs())
    except Exception as exc:
        await message.answer(**text)


# ==================== Earn
@router.message(~IsAdmin(), IsBanUser(), F.text == 'Заработать 💎')
@decorate_logging
async def user_earn_command(message: Message) -> None:
    """Earn Command Reply"""
    await delete_before_message(message)
    buttons = await user_reply_keyboard.earn_reply_keyboard()
    await message.answer(
        user_text.EARN_TEXT,
        reply_markup=buttons,
        parse_mode=ParseMode.HTML,
    )


@router.message(~IsAdmin(), IsBanUser(), F.text == '➕ Предложить материал')
@decorate_logging
async def user_offer_material_command(message: Message) -> None:
    """Offer Material Reply"""
    await message.answer(**user_text.OFFER_MATERIAL_TEXT.as_kwargs())


@router.message(~IsAdmin(), IsBanUser(), F.text == 'Пригласить друга 👥')
@decorate_logging
async def user_invite_friend_command(message: Message, session: AsyncSession) -> None:
    """Invite Friend Reply"""
    referral_nums: tuple[Any] | None = await services.get_referral_earned(message.from_user.id, session)
    if referral_nums:
        count_referral: int = referral_nums[1]
        earn_money: int = referral_nums[2]
    else:
        count_referral, earn_money = 0, 0

    text = user_text.INVITE_FRIEND_TEXT.format(
        bot_username=settings.BOT_USERNAME,
        referral_link=message.from_user.id,
        count_referral=count_referral,
        earn_money=earn_money,
    )
    await message.answer(text, parse_mode=ParseMode.HTML)


@router.message(~IsAdmin(), IsBanUser(), F.text == 'Получить бонус 🎁')
@decorate_logging
async def user_get_bonus_command(message: Message, state: FSMContext) -> None:
    """Get Bonus Reply"""
    await delete_before_message(message)
    await state.set_state(user_state.VerifyCodeState.code)

    button_verif = await user_inline_keyboard.pass_verification_inline_keyboard()
    button_cancel = await user_reply_keyboard.cancel_reply_command()
    await message.answer(user_text.GET_BONUS_TEXT_ONE, reply_markup=button_verif, parse_mode=ParseMode.HTML)
    await message.answer(user_text.GET_BONUS_TEXT_TWO, reply_markup=button_cancel, parse_mode=ParseMode.HTML)


@router.message(~IsAdmin(), IsBanUser(), user_state.VerifyCodeState.code, F.text != 'Отмена ❌')
@decorate_logging
async def user_get_bonus_message(message: Message, state: FSMContext) -> None:
    """Get Bonus Message"""
    bot_code: int = 100000
    text: dict[str, Any] = user_text.GET_BONUS_INVALID_CODE.as_kwargs()
    try:
        # Check Is Number and Positive
        if not await check_is_digit(message.text):
            await message.answer(**text)
            return
        # Check Equal Bot Code
        if int(message.text) != bot_code:
            await message.answer(**text)
            return
        # Clear State
        await state.clear()
    except Exception as exc:
        await message.answer(**text)
        return


# ==================== Premium
@router.message(~IsAdmin(), IsBanUser(), F.text == 'Premium-Подписка 🌟')
@decorate_logging
async def user_premium_subscribe_command(message: Message, session: AsyncSession) -> None:
    """Premium Subscribe Command Reply"""
    # Get Premium Price
    price: int = await services.get_premium_price(session)
    if not price:
        await message.answer(**user_text.PREMIUM_PRICE_DONT_SET.as_kwargs())
        return

    buttons = await user_reply_keyboard.premium_subscribe_reply_keyboard()
    await message.answer(
        user_text.PREMIUM_SUBSCRIBE_USER_TEXT.format(price=price, price_before=price + 200),
        reply_markup=buttons,
        parse_mode=ParseMode.HTML,
    )


@router.message(~IsAdmin(), IsBanUser(), F.text == '💫 Купить Premium-подписку')
@decorate_logging
async def user_premium_subscribe_buy_step_1(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """Buy Premium Step 1 Subscribe Command Reply"""
    # Get Premium Price
    price: int = await services.get_premium_price(session)
    # Set State
    await state.set_state(user_state.TransactionPay.pay_method)
    await state.update_data(type_pay='Премиум', sum=price)

    buttons = await user_inline_keyboard.payments_choose_inline_keyboard()
    await message.answer(**user_text.CHOOSE_PAYMENT_TEXT.as_kwargs(), reply_markup=buttons)


@router.callback_query(~IsAdmin(), IsBanUser(), user_state.TransactionPay.pay_method, F.data.startswith('premium_pay'))
@decorate_logging
async def user_premium_subscribe_buy_step_2(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Buy Premium Step 2 Command Inline"""
    pay_method: str = callback.data.split('_')[-1]
    # Get State Data
    await state.update_data(pay_method=PAYMENT_METHOD.get(pay_method))
    data = await state.get_data()
    await state.clear()

    # Create Transaction
    transaction_id: int = await services.create_transaction(callback.from_user.id, session, **data)
    # Output Information
    text: str = await user_text.show_window_pay_text(data['type_pay'], transaction_id, data['sum'])
    buttons = await user_inline_keyboard.payments_actions_buttons_inline_keyboard()
    await callback.message.answer(
        text,
        reply_markup=buttons,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


@router.callback_query(~IsAdmin(), IsBanUser(), user_state.TransactionPay.sum, F.data.startswith('check_pay'))
@decorate_logging
async def user_payment_check(callback: CallbackQuery) -> None:
    """Check Status Payment Command Inline"""
    await callback.answer(user_text.SHOW_PAYMENT_STATUS, show_alert=True)


@router.callback_query(~IsAdmin(), IsBanUser(), F.data == 'cancel_pay')
@decorate_logging
async def user_payment_cancel(callback: CallbackQuery, session: AsyncSession) -> None:
    """Cancel Payment Command Inline"""
    await user_start_command(callback.message, session)


# ==================== Categories
@router.message(~IsAdmin(), IsBanUser(), F.text == 'Категории 🔥')
@decorate_logging
async def user_categories_command(message: Message) -> None:
    """Categories Command Reply"""
    buttons = await user_reply_keyboard.categories_reply_command()
    await message.answer(user_text.CATEGORIES_TEXT, reply_markup=buttons, parse_mode=ParseMode.HTML)
