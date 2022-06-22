from aiogram.types import BotCommand

async def set_default_commands(dp):
    commands = [
        BotCommand(command="start",
            description="Приветсвие"),
        BotCommand(command="tasks",
            description="Получить файл с заданиями"),
        BotCommand(command="users",
            description="Получить файл с пользователями"),
         BotCommand(command="commands",
            description="Получить файл с командами"),
         BotCommand(command="dirs",
            description="Получить файл с директориями"),
         BotCommand(command="access",
            description="Получить файл с правами"),
           ]

    await dp.bot.set_my_commands(commands)
