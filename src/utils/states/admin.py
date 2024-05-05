from aiogram.fsm.state import StatesGroup, State


class PriceState(StatesGroup):
    price = State()
    action = State()


class FileState(StatesGroup):
    files = State()
    type_file = State()


class TechSupportState(StatesGroup):
    username = State()
    action = State()


class NotificationState(StatesGroup):
    message = State()
