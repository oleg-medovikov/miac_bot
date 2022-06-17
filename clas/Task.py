from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID

from conf import MIAC_API_URL, TOKEN
import requests

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
        URL = MIAC_API_URL + '/add_task'
        req = requests.post(URL, headers=HEADERS, json=BODY)

    def start(self):
        """Начать выполнение задачи"""
        HEADERS = dict(
            KEY = TOKEN
                )
        BODY = self.__dict__
        URL = MIAC_API_URL + '/start_task'
        req = requests.post(URL, headers=HEADERS, json=BODY)

    def get():
        """Взять доступную задачу"""
        HEADERS = dict(
            KEY = TOKEN
                )
        URL = MIAC_API_URL + '/get_task'
        req = requests.get(URL, headers=HEADERS)
        return req.json()

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
        req = requests.get(URL, headers=HEADERS)
 
    def stop(self):
        """Закончить задачу"""
        HEADERS = dict(
            KEY = TOKEN
                )
        BODY = self.__dict__
        URL = MIAC_API_URL + '/stop_task'
        req = requests.post(URL, headers=HEADERS, json=BODY)

    def users(self):
        """Получить список юзеров для рассылки"""
        HEADERS = dict(
            KEY = TOKEN
                )
        BODY = self.__dict__
        URL = MIAC_API_URL + '/get_task_users_list'
        req = requests.get(URL, headers=HEADERS, json=BODY)
        
        return req.json()

