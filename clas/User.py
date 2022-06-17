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

    def add(self, USER_ID ):
        "Добавление пользователя в таблицу пользователей"
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(USER_ID)
                )
        BODY = self.__dict__
        URL = MIAC_API_URL + '/add_user'

        req = requests.post(URL, headers=HEADERS, json=BODY )
  
    def get_by_id( USER_ID ):
        "Взять пользователя по id"
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(USER_ID)
                )
        URL = MIAC_API_URL + '/get_user_by_id'

        req = requests.get(URL, headers=HEADERS )
        
        if not req.json() is None:
            return User(**req.json())

    def check(self) -> bool:
        "Проверка пользователя на наличие в базе"
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(self.u_id)
                )
        URL = MIAC_API_URL + '/is_known'

        req = requests.get(URL, headers=HEADERS )
 
        return req.json()

    def admin(self) -> bool:
        "Проверка на администратора"
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(self.u_id)
                )
        URL = MIAC_API_URL + '/is_admin'

        req = requests.get(URL, headers=HEADERS )
 
        return req.json()

    def access(self):
        "Возвращает список доступных комманд"
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(self.u_id)
                )
        URL = MIAC_API_URL + '/user_commands'

        req = requests.get(URL, headers=HEADERS )
 
        return req.json()

    def get_all(USER_ID):
        "Получить всех пользователей"
        HEADERS = dict(
                KEY = TOKEN,
                UID = str( USER_ID )
                )
        URL = MIAC_API_URL + '/get_all_users'

        req = requests.get(URL, headers=HEADERS )
 
        return req.json()



