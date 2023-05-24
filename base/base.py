from databases import Database
from sqlalchemy import create_engine, MetaData

from conf import DATABASE_POSTGRESS

BASE = Database(DATABASE_POSTGRESS)
metadata = MetaData()
POSTGRESS_EN = create_engine(DATABASE_POSTGRESS)
