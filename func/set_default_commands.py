from aiogram.types import BotCommand


async def set_default_commands(dp):
    DICT = {
        "start": "Приветствие",
        "tasks": "Получить файл с заданиями",
        "users": "Получить файл с пользователями",
        "commands": "Получить файл с командами",
        "dirs": "Получить файл с директориями",
        "access": "Получить файл с правами",
            }

    commands = []
    for key, value in DICT.items():
        commands.append(BotCommand(
            command=key,
            description=value
            ))

    await dp.bot.set_my_commands(commands)
