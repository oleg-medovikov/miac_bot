from pydantic import BaseModel

from conf import MIAC_API_URL, TOKEN
import requests
from base import BASE, t_dirs


class Dir(BaseModel):
    d_id:         int
    d_name:       str
    directory:    str
    description:  str
    working:      bool


    def get( NAME ) -> str:
        "Получить директорию по имени"
        HEADERS = dict(
                KEY = TOKEN,
                )
        URL = MIAC_API_URL + '/get_dir'

        req = requests.get(URL, headers=HEADERS, json = NAME)
        
        return req.json()

    def add(self, USER_ID ):
        "Добавляем новую директорию"
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(USER_ID)
                )
        URL = MIAC_API_URL + '/add_dir'
        BODY = self.__dict__

        requests.post(URL, headers=HEADERS, json = BODY)

    async def get_all():
        "Получить все директории"
        query = t_dirs.select().order_by(t_dirs.c.d_id)
        return [dict(row) for row in await BASE.fetch_all(query)]
