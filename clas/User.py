from datetime import date
from uuid import uuid4, UUID
from pydantic import BaseModel

from base import POSTGRESS_DB, t_users, t_people

class User(BaseModel):
    u_id        : int
    first_name  : str
    last_name   : str
    username    : str
    groups      : str
    fio         : str
    description : str

    async def add(self):
        "Добавление пользователя в таблицу пользователей"
        
        query = t_users.select(t_users.c.u_id == self.u_id)
        res = await POSTGRESS_DB.fetch_one(query)

        if not res is None:
            query = t_users.delete(t_users.c.u_id == self.u_id)
            await POSTGRESS_DB.execute(query)

        query = t_users.insert().values(self.__dict__)
        await POSTGRESS_DB.execute(query)

    async def add_people(self):
        "Добавим людей которые писали боту"
        query = t_people.select(t_people.c.u_id == self.u_id)
        
        res = await POSTGRESS_DB.fetch_one(query)

        if res is None:
            MAN = self.__dict__
            MAN.drop('groups')
            MAN.drop('fio')
            MAN.drop('description')
            query = t_people.insert().values(MAN)
            await POSTGRESS_DB.execute(query)
    
    async def get_by_id(U_ID):
        "Взять пользователя по id"
        query = t_users.select(t_users.c.u_id == U_ID)

        res = await POSTGRESS_DB.fetch_one(query)

        if not res is None:
            return User(**res)


    async def check(self) -> bool:
        "Проверка пользователя на наличие в базе"
        query = t_users.select(t_users.c.u_id == self.u_id )

        res = await POSTGRESS_DB.fetch_one(query)

        if not res is None:
            return True
        else:
            return False

    async def admin(self) -> bool:
        "Проверка на администратора"
        query = t_users.select(t_users.c.u_id == self.u_id)

        res = await POSTGRESS_DB.fetch_one(query)

        if res is None:
            return False

        if res['groups'] == 'admin':
            return True
        else:
            return False
