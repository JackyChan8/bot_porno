from typing import Literal, get_args

from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, BigInteger, Text, Boolean, ForeignKey, TIMESTAMP, Enum

from .base_class import Base


TypeFile = Literal['фото', 'видео']
TypePay = Literal['Баланс', 'Премиум']
PaymentMethod = Literal['Карты', 'СБП | Скины | Крипта', 'Админ', 'CryptoBot']


class Users(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    is_ban: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now())

    balance = relationship("Balance", uselist=False, back_populates="user")
    premium = relationship("Premium", uselist=False, back_populates="user")


class Balance(Base):
    balance_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), unique=True)
    user_balance: Mapped[int] = mapped_column(Integer, default=5)

    user = relationship("Users", back_populates="balance")


class Premium(Base):
    premium_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), unique=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now())

    user = relationship("Users", back_populates="premium")


class Photos(Base):
    photo_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    is_publish: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now())


class Videos(Base):
    video_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    is_publish: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now())


class Actions(Base):
    action_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type_file: Mapped[TypeFile] = mapped_column(Enum(
        *get_args(TypeFile),
        name='typefile',
        create_constraint=True,
        validate_strings=True,
    ), default=get_args(TypeFile)[0])
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now())


class ReferralSystem(Base):
    referral_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), unique=True)
    referral_user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now())


class Bonus(Base):
    bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    code: Mapped[int] = mapped_column(BigInteger, nullable=False)


class Transactions(Base):
    transaction_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    sum: Mapped[int] = mapped_column(Integer)
    type_pay: Mapped[TypePay] = mapped_column(Enum(
        *get_args(TypePay),
        name='typepay',
        create_constraint=True,
        validate_strings=True,
    ), default=get_args(TypePay)[0])
    pay_method: Mapped[PaymentMethod] = mapped_column(Enum(
        *get_args(PaymentMethod),
        name='paymentmethod',
        create_constraint=True,
        validate_strings=True,
    ), default=get_args(PaymentMethod)[0])
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now())


class PremiumPrice(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    price: Mapped[int] = mapped_column(Integer, default=300)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.now())


class TechSupport(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
