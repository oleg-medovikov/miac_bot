from .dispetcher import  dp, bot 
from .on_startup import on_startup

from .start         import *
from .users_file    import *
from .commands_file import *
from .dirs_file     import *
from .access_file   import *
from .logs          import *
from .zamechania    import *

from .get_files import get_files

__all__ = [
    'dp',
    'bot',
    'on_startup',
    'get_files',
]
