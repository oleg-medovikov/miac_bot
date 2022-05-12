from .postgress import metadata, POSTGRESS_DB, POSTGRESS_EN
from .users import t_users
from .people import t_people
from .commands import t_commands
from .dirs import t_dirs


metadata.create_all(POSTGRESS_EN)
