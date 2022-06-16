from pydantic import BaseModel

from conf import MIAC_API_URL, TOKEN
import requests

class Dir(BaseModel):
    d_id        : int
    d_name      : str
    directory   : str
    description : str
    working     : bool


    async def get(NAME, USER_ID) -> str:
        "Получить директорию по имени"
        HEADERS = dict(
                KEY = TOKEN,
                UID = USER_ID
                )
        URL = MIAC_API_URL + '/get_dir'

        req = requests.get(URL, headers=HEADERS, json = NAME)
        
        return req.json()

    async def add(self):
        "Добавляем новую директорию"
        HEADERS = dict(
                KEY = TOKEN,
                UID = USER_ID
                )
        URL = MIAC_API_URL + '/add_dir'
        BODY = self.__dict__

        requests.post(URL, headers=HEADERS, json = BODY)
