from .base import metadata, POSTGRESS_DB, POSTGRESS_EN

# Таблицы обеспечивающие работу бота
from .users import t_users
from .people import t_people
from .commands import t_commands
from .dirs import t_dirs
from .access import t_access
from .tasks import t_tasks
from .choice import t_choice

metadata.create_all(POSTGRESS_EN)

__all__ = [
    'metadata',
    'POSTGRESS_DB',
    'POSTGRESS_EN',
    't_users',
    't_people',
    't_commands',
    't_dirs',
    't_access',
    't_tasks',
    't_choice',
]
