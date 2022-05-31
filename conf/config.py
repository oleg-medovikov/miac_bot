from starlette.config import Config

config = Config('.conf')

DATABASE_POSTGRESS = config('DATABASE_POSTGRESS', cast=str)

TELEGRAM_API   = config('TELEGRAM_API',   cast=str)
CHAT_SVALKA_ID = config('chat_svalka_id', cast=int)

DATABASE_PARUS  = config('DATABASE_PARUS',  cast=str)
ORACLE_HOME     = config('ORACLE_HOME',     cast=str)
LD_LIBRARY_PATH = config('LD_LIBRARY_PATH', cast=str)

DATABASE_COVID     = config('DATABASE_COVID',    cast=str)
DATABASE_MIAC_DS   = config('DATABASE_MIAC_DS',  cast=str)
DATABASE_NSI       = config('DATABASE_NSI',      cast=str)

URL_870 = config('URL_870', cast=str)

