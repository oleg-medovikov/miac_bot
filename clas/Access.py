from pydantic import BaseModel, Field

from conf import MIAC_API_URL, TOKEN

class Access(BaseModel):
    u_id : int
    c_id : int
    comment : str

    def get_all(USER_ID):
        "Забираем из базы все доступы с пояснениями"
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(USER_ID)
                )
        URL = MIAC_API_URL + '/get_access'

        req = requests.get(URL, headers=HEADERS )
        
        return req.json()


    def add(self, USER_ID):
        "Добавление доступа к комманде"
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(USER_ID)
                )
        BODY = self.__dict__
        URL = MIAC_API_URL + '/add_access'

        req = requests.post(URL, headers=HEADERS, json=BODY )

    def delete_all(USER_ID):
        HEADERS = dict(
                KEY = TOKEN,
                UID = str(USER_ID)
                )
        URL = MIAC_API_URL + '/delete_all_access'

        req = requests.delete(URL, headers=HEADERS)


