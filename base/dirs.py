from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Boolean

t_dirs = Table(
    "dirs",
    metadata,
    Column('d_id', Integer),        # номер директории
    Column('d_name', String),       # имя директории
    Column('directory', String),    # сама директория
    Column('description', String),  # пояснение
    Column('working', Boolean),     # Рабочая ли она
    )
