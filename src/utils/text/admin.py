from aiogram.utils.formatting import Bold

START_ADMIN_TEXT = '👋 Добро пожаловать в админку! 👋'
CHOOSE_COMMAND = '<b>Выберите подходящую команду</b>'
PLEASE_WAIT = '<b>Пожалуйста подождите...</b>'

# ======================================================== Users
NOT_EXIST_USERS_TEXT = '<b>Пользователи отсутствуют</b>'


async def blocking_user(is_block: bool) -> str:
    text = 'Заблокирован' if is_block else 'Разблокирован'
    return f'<b>🎉 Пользователь {text} 🎉</b>'

# ======================================================== Files
ADD_PHOTO_TEXT = '<b>Добавьте фотографии. ❗️ Общее кол-ва фотографий, которые можно добавить за раз 10 штук. ❗️</b>'
ADD_PHOTOS_SUCCESS_TEXT = '<b>🎉 Фотографии успешно добвлены 🎉</b>'
NOT_EXIST_FILES_TEXT = '<b>Файлы отсутствуют</b>'
FILE_SUCCESS_DELETED = '<b>🎉 Файл успешно удален 🎉</b>'


async def add_file_text(type_file: str) -> str:
    type_: str = 'фотографии' if type_file == 'photo' else 'видео'
    return f'<b>Добавьте {type_}. ❗️ Общее кол-ва {type_}, которые можно добавить за раз 10 штук. ❗️</b>'

# ======================================================== Videos
ADD_VIDEO_TEXT = '<b>Добавьте видео. ❗️ Общее кол-ва видео, которые можно добавить за раз 10 штук. ❗️</b>'
ADD_VIDEOS_SUCCESS_TEXT = '<b>🎉 Видео успешно добвлены 🎉</b>'
# ======================================================== Prices
SUCCESS_CREATE_PRICE = '🎉 Цена успешно изменена 🎉'
WRITE_PRICE = '<b>Напишите цену</b>'
WRITE_PRICE_INCORRECT_SUM = Bold('❗️ Введите коректную сумму для вывода')
SHOW_PRICE = '<b>Ваша Цена:</b> <code>{price}</code>'
# ======================================================== Prices
SUCCESS_CREATE_SUPPORT = '🎉 Тех.Поддержка успешно установлена 🎉'
WRITE_USERNAME_SUPPORT = '<b>Напишите Username пользователя Тех.Поддержки.</b>'
WRITE_USERNAME_INCORRECT = Bold('❗️ Введите коректное имя пользователя')
SHOW_TECH_SUPPORT = '<b>Имя Пользователя:</b> <code>{username}</code>'
