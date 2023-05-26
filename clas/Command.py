from pydantic import BaseModel

from conf import MIAC_API_URL, TOKEN
import requests

from base import BASE, t_commands


class Command(BaseModel):
    c_id:        int
    c_category:  str
    c_name:      str
    c_procedure: str
    c_arg:       str
    return_file: bool
    asc_day:     bool

    def add(self, USER_ID):
        "добавление новой команды"
        HEADERS = dict(
                KEY=TOKEN,
                UID=str(USER_ID) )
        BODY = self.__dict__
        URL = MIAC_API_URL + '/add_command'
        req = requests.post(URL,headers=HEADERS, json = BODY)

        return req.json()

    async def get_all():
        "Получение всех комманд"
        query = t_commands.select().order_by(t_commands.c.c_id)
        return [dict(row) for row in await BASE.fetch_all(query)]


    def get(C_ID):
        "Получение команды по айдишнику"
        HEADERS = dict(
                KEY=TOKEN,
                CID=str(C_ID) )

        URL = MIAC_API_URL + '/get_command'
        req  = requests.get(URL,headers=HEADERS)
        
        if not req.json() is None:
            return Command(**req.json())
