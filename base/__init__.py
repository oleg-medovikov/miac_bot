from .postgress import metadata, POSTGRESS_DB, POSTGRESS_EN
# работа с Парусом
from .parus import parus_sql
# Работа с COVID 
from .covid import covid_sql, covid_exec, covid_insert
# Работа с NsiBase
from .nsibase import nsi_sql


# Таблицы обеспечивающие работу бота
from .users     import t_users
from .people    import t_people
from .commands  import t_commands
from .dirs      import t_dirs
from .access    import t_access
from .tasks     import t_tasks
from .choice    import t_choice 

metadata.create_all(POSTGRESS_EN)
