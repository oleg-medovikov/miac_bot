from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID

from conf import MIAC_API_URL, TOKEN
from func import functions
import requests

class my_except(Exception):
    pass

class Task(BaseModel):
    t_id        : UUID = Field(default_factory=uuid4)
    time_create : datetime
    client      : int
    task_type   : str
    c_id        : int
    c_func      : str
    c_arg       : str
    users_list  : str
    time_start  : Optional[datetime]
    time_stop   : Optional[datetime]
    comment     : Optional[str]

    def add(self):
        """Создание нового задания
            Нужно проверить, есть ли в пуле 
            выполняющиеся такое задание"""
        HEADERS = dict(
            KEY = TOKEN,
            UID = str(self.client),
                )
        BODY = self.__dict__
        BODY['t_id'] = BODY['t_id'].hex
        BODY['time_create'] = BODY['time_create'].isoformat()

        URL = MIAC_API_URL + '/add_task'
        req = requests.post(URL, headers=HEADERS, json=BODY)
        return req.json()

    async def start(self):
        """Начать выполнение задачи"""
        
        if self.c_arg == 'no':
            FUNC = functions[self.c_func]()
        else:
            FUNC = functions[self.c_func](self.c_arg)

        try:
            RES = await FUNC
        except Exception as e:
            raise my_except(str(e))
        else:
            return RES


    def get():
        """Взять доступную задачу"""
        HEADERS = dict(
            KEY = TOKEN
                )
        URL = MIAC_API_URL + '/get_task'
        req = requests.get(URL, headers=HEADERS)
        
        if not req.json() is None:
            #print(req.json() )
            return Task(**req.json())

    def get_all_tasks(USER_ID):
        """Взять доступную задачу"""
        HEADERS = dict(
            KEY = TOKEN,
            UID = str(USER_ID)
                )
        URL = MIAC_API_URL + '/get_all_tasks'
        req = requests.get(URL, headers=HEADERS)
        return req.json()

    def restart():
        """Рестартануть выполнение задач, если бот перезапустился"""
        HEADERS = dict(
            KEY = TOKEN
                )
        URL = MIAC_API_URL + '/restart_tasks'
        req = requests.post(URL, headers=HEADERS)
 
    def stop(self):
        """Закончить задачу"""
        HEADERS = dict(
            KEY = TOKEN
                )
        BODY = self.__dict__

        try:
            BODY['t_id'] = BODY['t_id'].hex
        except:
            pass
        try:
            BODY['time_create'] = BODY['time_create'].isoformat()
        except:
            pass
        URL = MIAC_API_URL + '/stop_task'
        req = requests.post(URL, headers=HEADERS, json=BODY)

    def users(self):
        """Получить список юзеров для рассылки"""
        HEADERS = dict(
            KEY = TOKEN
                )
        BODY = self.__dict__
        BODY['t_id'] = BODY['t_id'].hex
        BODY['time_create'] = BODY['time_create'].isoformat()
        #BODY['time_start']  = BODY['time_start'].isoformat()
        
        URL = MIAC_API_URL + '/get_task_users_list'
        req = requests.get(URL, headers=HEADERS, json=BODY)
        
        return req.json()

