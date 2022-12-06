import asyncio
import aioschedule
import datetime

from clas import Task
from conf import MASTER, SVETLICHNAIA  # , KUZMINA


async def scheduler():
    aioschedule.every().day.at('01:00').do(load_fr)
    aioschedule.every().day.at('04:00').do(load_fr_death)
    aioschedule.every().day.at('05:00').do(load_umsrs)
    aioschedule.every().day.at('06:00').do(send_count_hospitalised)
    aioschedule.every().day.at('07:00').do(medical_personal_sick)
    aioschedule.every().day.at('21:00').do(send_file_uic)
    aioschedule.every().day.at('21:00').do(do_svod_death)
    aioschedule.every().thursday.at('11:00').do(send_otchet_deti)
    aioschedule.every().monday.at('10:00').do(send_otchet_po_ymershim)
    aioschedule.every().day.at('22:00').do(sbor_zabolevshie_med)
#    aioschedule.every().monday.at('12:00').do(send_compliment)
#   aioschedule.every(1).minutes.do(test_send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def send_compliment():
    TASK = Task(**{
        'time_create': datetime.datetime.now(),
        'client':      MASTER,
        'task_type':   'Sheduler',
        'c_id':        54,
        'c_func':      'get_compliments',
        'c_arg':       'no',
        'users_list':  str(MASTER),
        'time_start':  None,
        'time_stop':   None,
        'comment':     None
        })
    TASK.add()


async def medical_personal_sick():
    TASK = Task(**{
        'time_create':  datetime.datetime.now(),
        'client':       MASTER,
        'task_type':    'Sheduler',
        'c_id':         62,
        'c_func':       'medical_personal_sick',
        'c_arg':        'no',
        'users_list':   str(MASTER),
        'time_start':   None,
        'time_stop':    None,
        'comment':      None
        })
    TASK.add()


async def sbor_zabolevshie_med():
    TASK = Task(**{
        'time_create':  datetime.datetime.now(),
        'client':       MASTER,
        'task_type':    'Sheduler',
        'c_id':         60,
        'c_func':       'sbor_zabolevshix',
        'c_arg':        'no',
        'users_list':   str(MASTER),
        'time_start':   None,
        'time_stop':    None,
        'comment':      None
        })
    TASK.add()


async def send_otchet_po_ymershim():
    TASK = Task(**{
        'time_create': datetime.datetime.now(),
        'client':      MASTER,
        'task_type':   'Sheduler',
        'c_id':        59,
        'c_func':      'otchet_po_ymershim',
        'c_arg':       'no',
        'users_list':  str(MASTER),
        'time_start':  None,
        'time_stop':   None,
        'comment':     None
        })
    TASK.add()


async def send_otchet_deti():
    TASK = Task(**{
        'time_create': datetime.datetime.now(),
        'client':      SVETLICHNAIA,
        'task_type':   'Sheduler',
        'c_id':        58,
        'c_func':      'send_otchet_deti',
        'c_arg':       'no',
        'users_list':  str(SVETLICHNAIA),
        'time_start':  None,
        'time_stop':   None,
        'comment':     None
        })
    TASK.add()


async def do_svod_death():
    TASK = Task(**{
        'time_create': datetime.datetime.now(),
        'client':      SVETLICHNAIA,
        'task_type':   'Sheduler',
        'c_id':        57,
        'c_func':      'svod_death',
        'c_arg':       'no',
        'users_list':  str(SVETLICHNAIA),
        'time_start':  None,
        'time_stop':   None,
        'comment':     None
        })
    TASK.add()


async def send_count_hospitalised():
    TASK = Task(**{
        'time_create': datetime.datetime.now(),
        'client':      SVETLICHNAIA,
        'task_type':   'Sheduler',
        'c_id':        52,
        'c_func':      'hospitalised_in_fr',
        'c_arg':       'no',
        'users_list':  str(SVETLICHNAIA),
        'time_start':  None,
        'time_stop':   None,
        'comment':     None
        })
    TASK.add()


async def send_file_uic():
    TASK = Task(**{
        'time_create':  datetime.datetime.now(),
        'client':       MASTER,
        'task_type':    'Sheduler',
        'c_id':         50,
        'c_func':       'copy_uach',
        'c_arg':        'no',
        'users_list':   str(MASTER),
        'time_start':   None,
        'time_stop':    None,
        'comment':      None
        })
    TASK.add()


async def load_fr():
    TASK = Task(**{
        'time_create':  datetime.datetime.now(),
        'client':       MASTER,
        'task_type':    'Sheduler',
        'c_id':         41,
        'c_func':       'load_fr',
        'c_arg':        'no',
        'users_list':   str(MASTER),
        'time_start':   None,
        'time_stop':    None,
        'comment':      None
        })
    TASK.add()


async def load_fr_death():
    TASK = Task(**{
        'time_create':  datetime.datetime.now(),
        'client':       MASTER,
        'task_type':    'Sheduler',
        'c_id':         42,
        'c_func':       'load_fr_death',
        'c_arg':        'no',
        'users_list':   str(MASTER),
        'time_start':   None,
        'time_stop':    None,
        'comment':      None
        })
    TASK.add()


async def load_umsrs():
    TASK = Task(**{
        'time_create':  datetime.datetime.now(),
        'client':       MASTER,
        'task_type':    'Sheduler',
        'c_id':         43,
        'c_func':       'load_umsrs',
        'c_arg':        'no',
        'users_list':   str(MASTER),
        'time_start':   None,
        'time_stop':    None,
        'comment':      None
        })
    TASK.add()
