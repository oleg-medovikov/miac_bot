from pydantic import BaseModel

from conf import MIAC_API_URL, TOKEN
import requests
from base import BASE, t_access, t_users, t_commands
from sqlalchemy import select


class Access(BaseModel):
    u_id:    int
    c_id:    int
    comment: str

    @staticmethod
    async def get_all():
        "Забираем из базы все доступы с пояснениями"
        j = t_access.join(
            t_users,
            t_access.c.u_id == t_users.c.u_id
        ).join(
            t_commands,
            t_access.c.c_id == t_commands.c.c_id,
        )

        query = select([
            t_access.c.u_id,
            t_users.c.fio,
            t_access.c.c_id,
            t_commands.c.c_name,
            t_access.c.comment,
        ]).order_by(t_users.c.fio).select_from(j)

        res = await BASE.fetch_all(query)
        return [dict(r) for r in res]

    def add(self, USER_ID):
        "Добавление доступа к комманде"
        HEADERS = dict(
                KEY=TOKEN,
                UID=str(USER_ID)
                )
        BODY = self.__dict__
        URL = MIAC_API_URL + '/add_access'

        requests.post(URL, headers=HEADERS, json=BODY)

    def delete_all(USER_ID):
        HEADERS = dict(
                KEY=TOKEN,
                UID=str(USER_ID)
                )
        URL = MIAC_API_URL + '/delete_all_access'

        requests.delete(URL, headers=HEADERS)
