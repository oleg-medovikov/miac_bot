from disp import dp, on_startup
from aiogram import executor
import warnings

warnings.filterwarnings("ignore")

if __name__ == '__main__':
    executor.start_polling(
            dp,
            on_startup=on_startup,
            skip_updates=False)
