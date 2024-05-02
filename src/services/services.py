from typing import Any

from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import decorate_logging
from src.utils.text import admin as admin_text
from sqlalchemy import insert, select, update, exists, distinct, func, case, null, false, true
from src.models import (Users, Balance, Premium, Actions, Photos, Videos,
                        ReferralSystem, Transactions, PremiumPrice, TechSupport)


# ============================================== Users

@decorate_logging
async def check_exist_user(user_id: int, session: AsyncSession) -> bool:
    """Check Exist User Service"""
    result = await session.execute(
        select(exists(Users.user_id).where(Users.user_id == user_id))
    )
    return result.scalar()


@decorate_logging
async def check_is_blocked_users(user_id: int, session: AsyncSession) -> int:
    """Check Is Blocked Users Service"""
    query = (
        select(
            case(
                (
                    exists(
                        select(Users.user_id).where(
                            Users.user_id == user_id, Users.is_ban == true())
                    ), 1), else_=0
            )
        )
        .where(Users.user_id == user_id)
    )
    result = await session.execute(query)
    return result.scalar()


@decorate_logging
async def get_info_user(user_id: int, session: AsyncSession):
    """Get Information About User"""
    query = (
        select(
            Users.user_id,
            Users.is_ban,
            func.count(distinct(Actions.action_id)).filter(Actions.type_file == 'фото').label('count_watch_photo'),
            func.count(distinct(Actions.action_id)).filter(Actions.type_file == 'видео').label('count_watch_video'),
            case((Premium.premium_id.is_not(None), True), else_=False).label('exist_premium'),
            Balance.user_balance
        )
        .where(Users.user_id == user_id)
        .join(Balance, Users.user_id == Balance.user_id, isouter=True)
        .join(Actions, Users.user_id == Actions.user_id, isouter=True)
        .join(Premium, Users.user_id == Premium.user_id, isouter=True)
        .group_by(Users.user_id, 'exist_premium', Balance.user_balance)
    )
    result = await session.execute(query)
    return result.first()


@decorate_logging
async def get_count_users(*args, session: AsyncSession) -> int:
    """Get Count Users"""
    result = await session.execute(
        select(func.count('*')).select_from(Users)
    )
    return result.scalar()


@decorate_logging
async def get_users(*args, session: AsyncSession, offset: int = null(), limit: int = 3):
    """Get Users"""
    query = (
        select(Users.user_id)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(query)
    return result.scalars().all()


@decorate_logging
async def blocking_user(user_id: int, is_block: bool, message: Message, session: AsyncSession) -> bool:
    """Block User"""
    is_ban = true() if is_block else false()
    query = (
        update(Users)
        .where(Users.user_id == user_id)
        .values(is_ban=is_ban)
        .execution_options(synchronize_session='fetch')
    )
    try:
        await session.execute(query)
        await session.commit()

        text = await admin_text.blocking_user(is_block)
        await message.answer(text, parse_mode=ParseMode.HTML)
        return True
    except Exception:
        await session.rollback()
        return False


@decorate_logging
async def create_user(user_id: int, session: AsyncSession) -> None:
    """Create User Service"""
    try:
        user = Users(user_id=user_id)
        Balance(user=user)
        session.add(user)
        await session.commit()
    except Exception:
        await session.rollback()


# ============================================== Actions
@decorate_logging
async def create_action(user_id: int, type_file: str, filename: str, session: AsyncSession) -> None:
    """Create Action Service"""
    query = (
        insert(Actions)
        .values(
            type_file=type_file,
            filename=filename,
            user_id=user_id,
        )
    )
    try:
        await session.execute(query)
        await session.commit()
    except Exception:
        await session.rollback()


# ============================================== Update Balance
@decorate_logging
async def get_balance(user_id: int, session: AsyncSession) -> int:
    """Get Balance Service"""
    query = (
        select(Balance.user_balance)
        .where(Balance.user_id == user_id)
    )
    result = await session.execute(query)
    return result.scalar()


@decorate_logging
async def update_balance(user_id: int, operator: str, sum_num: int, session: AsyncSession) -> None:
    """Update Balance Service"""
    query = (
        update(Balance)
        .where(Balance.user_id == user_id)
        .values({'user_balance': Balance.user_balance + sum_num if operator == '+' else Balance.user_balance - sum_num})
        .execution_options(synchronize_session='fetch')
    )

    try:
        await session.execute(query)
        await session.commit()
    except Exception:
        await session.rollback()


# ============================================== Referral Link
@decorate_logging
async def get_referral_earned(user_id: int, session: AsyncSession, earn_ref: int = 10) -> tuple[Any] | None:
    """Get Referral Earned"""
    query = (
        select(
            ReferralSystem.referral_user_id,
            func.count(
                case((ReferralSystem.referral_id.is_not(None), 1), else_=0)
            ).label('count_referral'),
            func.sum(
                case((ReferralSystem.referral_id.is_not(None), earn_ref), else_=0)
            ).label('earn_money')
        )
        .select_from(ReferralSystem)
        .where(ReferralSystem.referral_user_id == user_id)
        .group_by(ReferralSystem.referral_user_id)
    )
    result = await session.execute(query)
    return result.first()


@decorate_logging
async def create_refer_link(user_id: int, referral_id: int, session: AsyncSession) -> bool:
    """Create Referral Link Service"""
    query = (
        insert(ReferralSystem)
        .values(
            user_id=user_id,
            referral_user_id=referral_id,
        )
    )
    try:
        await session.execute(query)
        await session.commit()
        return True
    except Exception:
        await session.rollback()
        return False


# ============================================== Transactions
@decorate_logging
async def create_transaction(user_id: int, session: AsyncSession, **kwargs) -> int:
    """Create Transaction Service"""
    query = (
        insert(Transactions)
        .values(user_id=user_id, **kwargs)
        .returning(Transactions.transaction_id)
    )
    try:
        result = await session.execute(query)
        await session.commit()
        return result.scalar()
    except Exception:
        await session.rollback()


# ============================================== Premium Price
@decorate_logging
async def check_exist_premium_price(session: AsyncSession) -> bool:
    """Check Exist Premium Price Service"""
    result = await session.execute(select(exists(PremiumPrice.id)))
    return result.scalar()


@decorate_logging
async def get_premium_price(session: AsyncSession) -> int:
    """Get Premium Price Service"""
    result = await session.execute(
        select(PremiumPrice.price)
    )
    return result.scalar()


@decorate_logging
async def update_premium_price(price: int, message: Message, session: AsyncSession) -> bool:
    """Update Premium Price Service"""
    query = (
        update(PremiumPrice)
        .where(PremiumPrice.id == 1)
        .values(price=price)
        .execution_options(synchronize_session='fetch')
    )
    try:
        await session.execute(query)
        await session.commit()
        await message.answer(admin_text.SUCCESS_CREATE_PRICE)
        return True
    except Exception:
        await session.rollback()
        return False


@decorate_logging
async def create_premium_price(price: int, message: Message, session: AsyncSession) -> bool:
    """Create Premium Price Service"""
    query = (
        insert(PremiumPrice)
        .values(price=price)
    )
    try:
        await session.execute(query)
        await session.commit()
        await message.answer(admin_text.SUCCESS_CREATE_PRICE)
        return True
    except Exception:
        await session.rollback()
        return False


# ============================================== Photos
@decorate_logging
async def delete_file(file_id: int, type_file: str, session: AsyncSession, message: Message) -> None:
    """Delete File"""
    table = Photos if type_file == 'фото' else Videos
    query = (
        update(table)
        .where(table.photo_id == file_id if type_file == 'фото' else table.video_id == file_id)
        .values(is_publish=false())
        .execution_options(synchronize_session='fetch')
    )
    try:
        await session.execute(query)
        await session.commit()
        await message.answer(admin_text.FILE_SUCCESS_DELETED, parse_mode=ParseMode.HTML)
    except Exception:
        await session.rollback()


@decorate_logging
async def create_file(files_name: list[str], type_file: str, session: AsyncSession, message: Message) -> bool:
    """Create File"""
    table = Photos if type_file == 'photo' else Videos
    text: str = admin_text.ADD_PHOTOS_SUCCESS_TEXT if type_file == 'photo' else admin_text.ADD_VIDEOS_SUCCESS_TEXT
    data: list[dict[str, str]] = [{'filename': filename} for filename in files_name]

    query = (
        insert(table)
        .values(data)
    )
    try:
        await session.execute(query)
        await session.commit()
        await message.answer(text, parse_mode=ParseMode.HTML)
        return True
    except Exception:
        await session.rollback()
        return False


@decorate_logging
async def get_count_files(type_file: str, session: AsyncSession) -> int:
    """Get Count Files"""
    table = Photos if type_file == 'фото' else Videos
    result = await session.execute(
        select(func.count('*')).select_from(table).where(table.is_publish == true())
    )
    return result.scalar()


@decorate_logging
async def get_files(type_file: str, session: AsyncSession, offset: int = null(), limit: int = 3):
    """Get Files"""
    table = Photos if type_file == 'фото' else Videos
    query = (
        select(
            table.photo_id if type_file == 'фото' else table.video_id,
        )
        .where(table.is_publish == true())
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(query)
    return result.scalars().all()


@decorate_logging
async def get_file_by_id(file_id: int, type_file: str, session: AsyncSession):
    """Get File By ID"""
    table = Photos if type_file == 'фото' else Videos
    query = (
        select(
            table.filename,
            table.created_at,
        )
        .where(table.photo_id == file_id if type_file == 'фото' else table.video_id == file_id)
    )
    result = await session.execute(query)
    return result.first()


@decorate_logging
async def get_random_file(user_id: int, type_file: str, session: AsyncSession, limit: int = 1) -> str | None:
    """Get Random File"""
    table = Photos if type_file == 'фото' else Videos

    query = (
        select(table.filename)
        .where(
            table.is_publish == true(),
            table.filename.not_in(
                select(Actions.filename).where(Actions.user_id == user_id)
            )
        )
        .limit(limit)
    )
    result = await session.execute(query)
    return result.scalar()


# ============================================== Tech Support
@decorate_logging
async def check_exist_tech_support(session: AsyncSession) -> bool:
    """Check Exist Tech Support Service"""
    result = await session.execute(select(exists(TechSupport.id)))
    return result.scalar()


@decorate_logging
async def get_tech_support(session: AsyncSession) -> str:
    """Get Tech Support"""
    result = await session.execute(
        select(TechSupport.username)
    )
    return result.scalar()


@decorate_logging
async def update_tech_support(username: str, message: Message, session: AsyncSession) -> bool:
    """Update Tech Support Service"""
    query = (
        update(TechSupport)
        .where(TechSupport.id == 1)
        .values(username=username)
        .execution_options(synchronize_session='fetch')
    )
    try:
        await session.execute(query)
        await session.commit()
        await message.answer(admin_text.SUCCESS_CREATE_SUPPORT)
        return True
    except Exception:
        await session.rollback()
        return False


@decorate_logging
async def create_tech_support(username: str, message: Message, session: AsyncSession) -> bool:
    """Create Tech Support Service"""
    query = (
        insert(TechSupport)
        .values(username=username)
    )
    try:
        await session.execute(query)
        await session.commit()
        await message.answer(admin_text.SUCCESS_CREATE_SUPPORT)
        return True
    except Exception:
        await session.rollback()
        return False
