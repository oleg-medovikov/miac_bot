from .postgress import metadata

from sqlalchemy import Table, Column,  String, Boolean
from sqlalchemy.dialects.postgresql import UUID

t_dirs = Table(
    "dirs",
    metadata,
    Column('d_name', String), # имя директории
    Column('directory', String), # сама директория
    Column('working', Boolean), # Рабочая ли она
    ) 
