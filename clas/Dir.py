from pydantic import BaseModel

from base import POSTGRESS_DB, t_dirs

class Dir(BaseModel):
    d_name    : str
    directory : str
    working   : bool

    async def get(NAME) -> str:
        "Получить директорию по имени"
        query = t_dirs.select(t_dirs.c.d_name == NAME)
        res = await POSTGRESS_DB.fetch_one(query)

        if not res is None and res['working']:
            return res['directory']
        else:
            return ''

