from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from src.utils.text.user import START_COMMAND


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description=START_COMMAND),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
