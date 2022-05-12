from datetime import date
from uuid import uuid4, UUID
from pydantic import BaseModel, Field

from base import POSTGRESS_DB, t_users, t_people

class User(BaseModel):
    u_id: int
    first_name : str
    last_name : str
    username : str

    async def add(self):
        "Добавление пользователя в таблицу пользователей"
        
        query = t_users.select(t_users.c.u_id == self.u_id)
        res = await POSTGRESS_DB.fetch_one(query)

        if not res is None:
            return 'Есть такой юзер'
        else:
            query = t_users.insert().values(self.__dict__)
            await POSTGRESS_DB.execute(query)

    async def add_people(self):
        "Добавим людей которые писали боту"
        query = t_people.select(t_people.c.u_id == self.u_id)
        
        res = await POSTGRESS_DB.fetch_one(query)

        if res is None:
            query = t_people.insert().values(self.__dict__)
            await POSTGRESS_DB.execute(query)

    async def check(self) -> bool:
        "Проверка пользователя на наличие в базе"
        query = t_users.select(t_users.c.u_id == self.u_id )

        res = await POSTGRESS_DB.fetch_one(query)

        if not res is None:
            return True
        else:
            return False

