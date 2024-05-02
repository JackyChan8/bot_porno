from aiogram.fsm.state import StatesGroup, State


class OutBalanceStates(StatesGroup):
    sum = State()


class VerifyCodeState(StatesGroup):
    code = State()


class TransactionPay(StatesGroup):
    pay_method = State()
    type_pay = State()
    sum = State()
