from pydantic import BaseModel

from conf import MIAC_API_URL, TOKEN
import requests 

class Choice(BaseModel):
    u_id : int
    c_id : int

    async def add(self):
        """Добавляем новый выбор пользователя"""

        HEADERS = dict(
                KEY = TOKEN,
                UID = str(self.u_id),
                CID = str(self.c_id)
                )

        URL = MIAC_API_URL + '/add_user_choice'

        requests.post(URL, headers=HEADERS )



    async def delete(self):
        """Удалить выбор пользователя"""
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(self.u_id)
                )

        URL = MIAC_API_URL + '/delete_user_choice'

        requests.delete(URL, headers=HEADERS )

   

    async def get(U_ID):
        """Получить выбор пользователя"""
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(self.u_id)
                )

        URL = MIAC_API_URL + '/get_user_choice'

        req = requests.get(URL, headers=HEADERS )

        return req.json()

 
