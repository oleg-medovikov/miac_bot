from .base import metadata

from sqlalchemy import Table, Column, String, BigInteger

t_users = Table(
    "users",
    metadata,
    Column('u_id', BigInteger),     # Идентификатор юзера в телеге
    Column('first_name', String),   # Имя юзера в телеге
    Column('last_name', String),    # Фамилия юзера в телеге
    Column('username', String),     # username юзера в телеге
    Column('groups', String),       # username юзера в телеге
    Column('fio', String),          # username юзера в телеге
    Column('description', String),  # Описание кто это такой
    )
