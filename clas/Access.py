from pydantic import BaseModel, Field

from conf import MIAC_API_URL, TOKEN

class Access(BaseModel):
    u_id : int
    c_id : int
    comment : str

    async def add(self, UID):
        "Добавление доступа к комманде"
        HEADERS = dict(
                KEY = TOKEN,
                UID = USER_ID
                )
        BODY = self.__dict__
        URL = MIAC_API_URL + '/add_access'

        req = requests.post(URL, headers=HEADERS, json=BODY )



    async def delete_all(UID):
        HEADERS = dict(
                KEY = TOKEN,
                UID = USER_ID
                )
        URL = MIAC_API_URL + '/delete_all_access'

        req = requests.delete(URL, headers=HEADERS)


