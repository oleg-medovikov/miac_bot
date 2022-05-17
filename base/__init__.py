from .postgress import metadata, POSTGRESS_DB, POSTGRESS_EN

# Таблицы обеспечивающие работу бота
from .users     import t_users
from .people    import t_people
from .commands  import t_commands
from .dirs      import t_dirs
from .access    import t_access


metadata.create_all(POSTGRESS_EN)
