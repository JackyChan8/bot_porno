from aiogram.utils.formatting import Bold

START_COMMAND = 'Запуск бота'

START_USER_TEXT = """
<b>👇 Выбери действие:</b>

<b>📷 Смотреть фото - 1 💎</b> 
<b>📹 Смотреть видео - 2 💎</b>
<b>⚜️ С Premium подпиской: 0 💎</b> за любое действие
*(+ улучшенная навигация и доступ к категориям)*
*(+ доступ к покупке категорий )*

<b>👫 Зарабатывай по 10 💎 (20 RUB) за каждого приглашенного друга и выводи на карту эти деньги!</b>
"""

# ======================================================== Watch Photo
WATCH_PHOTO_TEXT = """
🌇 Вот твоё случайное {type}
📊 Просмотрено: <b>1</b> из <b>11576</b>
"""


async def watch_file_text(type_file: str) -> str:
    type_ = 'фото' if type_file == 'photo' else 'видео'
    return WATCH_PHOTO_TEXT.format(type=type_)


WATCH_FILE_NOT_BALANCE = """
<b>❗️❗️ДЛЯ ТОГО ЧТОБЫ ИСПОЛЬЗОВАТЬ БОТА необходимо подписаться на новостной канал и  вступить в наш дружный чатик❗️❗️</b>

<i>Для этого нажми кнопку</i> "<b>➡️ Вступить</b>" <i>и после того как вступил нажми</i> "<b>Выполнено ✅</b>"
"""

WATCH_FILE_NOT_EXIST_FILE = '❗️ Больше нет файлов ❗️'
# ======================================================== Profile


async def profile_user_text(user_id: int,
                            cnt_photos: int,
                            cnt_videos: int,
                            is_premium: bool,
                            balance: int,
                            admin_username: str = '',
                            is_admin: bool = False) -> str:
    is_premium_text = 'активирована 🟢 ' if is_premium else 'не активирована 🔴'
    admin_text = '' if is_admin else f'<b>👩🏼‍💻 Администратор:</b> @{admin_username}'

    return PROFILE_USER_TEXT.format(
        user_id=user_id,
        cnt_photos=cnt_photos,
        cnt_videos=cnt_videos,
        is_premium=is_premium_text,
        balance=balance,
        admin_text=admin_text,
    )


PROFILE_USER_TEXT = """
<b>📱 Ваш профиль</b>

<b>🔑 ID:</b> <code>{user_id}</code>
<b>💎</b> Баланс: {balance}

<b>🌇 Просмотрено всего фото:</b> {cnt_photos}
<b>🎥 Просмотрено всего видео:</b> {cnt_videos}

<b>🌟 Premium-подписка:</b> {is_premium}
<b>🔥 Купленные категории:</b> <i>(Отсутствуют)</i>
{admin_text}
"""

PROFILE_TOP_UP_TEXT = """
<i>💸 Выберите сумму пополнения</i> <b>2 💎 = 1 RUB ⚡️ Первое</b> пополнение от <b>100 RUB</b> <i>по курсу</i> <b>1 RUB = 4 💎</b>
"""

PROFILE_OUT_BALANCE = Bold('💰Введите сумму для вывода:')
PROFILE_OUT_BALANCE_INCORRECT_SUM = Bold('❗️ Введите коректную сумму для вывода')
PROFILE_OUT_BALANCE_LESS = Bold('Минимальная сумма вывода средств 500 💎(1000 RUB)')
PROFILE_OUT_BALANCE_DONT_ENOUGH = Bold(
    '❗️ У вас недостаточно 💎 на балансе. Введите другую сумму, либо попробуйте заработать больше')

# ======================================================== Earn
EARN_TEXT = """
<b>👇 Выбери действие:</b>

<b>👥 Пригласить друга</b> - 10 💎 (20 RUB)🎁 <b>Получить бонус</b>  - 20 💎 (40 RUB)➕ <b>Предложить материал</b> - зависит от материалов

<i>Зарабатывай 💎 и выводи их на карту</i>
"""

OFFER_MATERIAL_TEXT = Bold('В данный момент мы не принимаем материалы!')
INVITE_FRIEND_TEXT = """
<b>🎁 Пригласи друга и получи 10 💎(20 RUB) за каждого приглашённого</b>

<b>📎 Нажми на ссылку для копирования 👇</b>
👉 <code>https://t.me/{bot_username}?start={referral_link}</code>

<b>📊 Статистика приглашенных пользователей:</b> <code>{count_referral}</code>
<b>💰 Заработано за приглашенных пользователей:</b> <code>{earn_money}</code> 💎

<b>✅ Ссылку можно отправлять своим друзьям, в чатах, или в анонимных чат ботах</b>
"""

GET_BONUS_TEXT_ONE = """
<b>🎁 Для получения бонуса в размере 40💎 необходимо:

✔️Пройти проверку
В связи с постоянной продажей наших фото/видео в посторонних источниках мы вынуждены проверить вас на человека.</b>
"""
GET_BONUS_TEXT_TWO = '👇 Пожалуйста отправьте <b>КОД</b> полученный в конце проверки:'
GET_BONUS_INVALID_CODE = Bold('❌ Неверный код проверки. Пожалуйста, попробуйте еще раз:')

# ======================================================== Premium Subscribe
PREMIUM_PRICE_DONT_SET = Bold("❗️ Цена Премиум Подписки не установлена ❗️")
PREMIUM_SUBSCRIBE_USER_TEXT = """
<b>❗️ ВНИМАНИЕ АКЦИЯ ❗️
🔥 Только до конца дня (до 23:59)
💵 Стоимость подписки всего: {price} RUB</b>(вместо {price_before} RUB)

<b>⚜️ Premium подписка:</b>
- неограниченный доступ(0💎 за просмотр)
- улучшенная навигация в разделах ⏮◀️▶️⏭
- возможность сохранять контент 🔐
- самый запрещенный и жаркий контент 🔞
<b>- Доступ к категориям 🔥
⚜️ Premium подписка активируется навсегда</b>

⚡️ Покупай сейчас и наслаждайся 💦
<b>👇 Нажми кнопку ниже для оплаты 👇</b>
"""

# ======================================================== Payment Text
CHOOSE_PAYMENT_TEXT = Bold('💸 Выберите способ оплаты:')
SHOW_WINDOW_PAY_TEXT = """
<b>{header_text}</b> #ID{transaction_id}
➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>🔮 Для {second_text}, нажмите на кнопку ниже</b>
<i><a href="https://aaio.so/merchant/pay?merchant_id=5dd149bc-0060-441f-bd7f-c8bdfca8c553&amount=300&currency=RUB&order_id=M%7C460287137&sign=a76f639a6dfed3ff92285128bcab704c94c265a1884a8501acd9b988d612af90&desc=Premium-subscribe+for+6433204230&lang=ru">Перейти к оплате</a></i> и оплатите выставленный вам счёт
<b>💰 Сумма {sum_text}:</b> <code>{sum_pay}₽</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>🔄 После оплаты, нажмите на</b> <code>Проверить оплату</code>
"""


async def show_window_pay_text(type_pay: str, transaction_id: int, sum_pay: int) -> str:
    if type_pay == 'Премиум':
        header_text: str = '🌟 Покупка Premium-подписки'
        second_text: str = 'оплаты подписки'
        sum_text: str = 'к оплате'
    else:
        header_text: str = '📈 Пополнение баланса'
        second_text: str = 'пополнения баланса'
        sum_text: str = 'пополнения'

    return SHOW_WINDOW_PAY_TEXT.format(
        header_text=header_text,
        transaction_id=transaction_id,
        second_text=second_text,
        sum_text=sum_text,
        sum_pay=sum_pay,
    )

SHOW_PAYMENT_STATUS = '🔴 Оплата не обнаружена или еще не дошла до нас'

CATEGORIES_TEXT = """
<b>📛 У вас нет доступа к категориям
Чтобы получить доступ к категориям необходимо приобрести Premium-подписку</b>
"""

# ======================================================== Referral Link
NOT_USE_SELF_REFERRAL_LINK = '❗️ Нельзя регистрироваться по собственной реферальной ссылке ❗️'
SUCCESS_CREATE_BY_REFERRAL_LINK = """
🎉 Пользователь @{username} успешно зарегистрировался в боте по вашей реферальной ссылке 🎉
"""
