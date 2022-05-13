from aiogram.types import BotCommand

async def set_default_commands(dp):
    commands = [
        BotCommand(command="start",
            description="Приветсвие"),
        BotCommand(command="commands",
            description="Получить файл с командами"),
         ]

    await dp.bot.set_my_commands(commands)
