from .base import metadata

from sqlalchemy import Table, Column, Integer, String, DateTime, BigInteger

t_active = Table(
    "active",
    metadata,
    Column('time', DateTime),  # Время события
    Column('u_id', BigInteger),  # номер юзера
    Column('event_type', String),  # тип события
    Column('c_id', Integer),  # номер команды
    Column('comment', String),  # комментарий
    )
