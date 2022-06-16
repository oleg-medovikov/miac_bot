from datetime import date
from uuid import uuid4, UUID
from pydantic import BaseModel
from typing import Optional

from conf import MIAC_API_URL, TOKEN
import requests 

class User(BaseModel):
    u_id        : int
    first_name  : Optional[str]
    last_name   : Optional[str]
    username    : Optional[str]
    groups      : str
    fio         : str
    description : str

    async def add(self, USER_ID ):
        "Добавление пользователя в таблицу пользователей"

        HEADERS = dict(
                KEY = TOKEN,
                UID = USER_ID
                )
        BODY = self.__dict__
        URL = MIAC_API_URL + '/add_user'

        req = requests.post(URL, headers=HEADERS, json=BODY )

"""
    async def add_people(self):
        "Добавим людей которые писали боту"
        query = t_people.select(t_people.c.u_id == self.u_id)
        
        res = await POSTGRESS_DB.fetch_one(query)

        if res is None:
            MAN = self.__dict__
            MAN.pop('groups')
            MAN.pop('fio')
            MAN.pop('description')
            query = t_people.insert().values(MAN)
            await POSTGRESS_DB.execute(query)
"""    
    async def get_by_id(U_ID):
        "Взять пользователя по id"
        HEADERS = dict(
                KEY = TOKEN,
                UID = USER_ID
                )
        URL = MIAC_API_URL + '/get_user_by_id'

        req = requests.get(URL, headers=HEADERS )
        
        if not req.json() is None:
            return User(**req.json())

    async def check(self) -> bool:
        "Проверка пользователя на наличие в базе"
        HEADERS = dict(
                KEY = TOKEN,
                UID = USER_ID
                )
        URL = MIAC_API_URL + '/is_known'

        req = requests.get(URL, headers=HEADERS )
 
        return req.json()

    async def admin(self) -> bool:
        "Проверка на администратора"
        HEADERS = dict(
                KEY = TOKEN,
                UID = USER_ID
                )
        URL = MIAC_API_URL + '/is_admin'

        req = requests.get(URL, headers=HEADERS )
 
        return req.json()

    async def access(self):
        "Возвращает список доступных комманд"
        HEADERS = dict(
                KEY = TOKEN,
                UID = USER_ID
                )
        URL = MIAC_API_URL + '/user_commands'

        req = requests.get(URL, headers=HEADERS )
 
        return req.json()
