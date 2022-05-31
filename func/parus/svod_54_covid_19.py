import time, datetime, shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql


async def svod_54_covid_19():
    SQL_1 = open('func/parus/sql/covid_54_svod.sql', 'r').read()
    #SQL_2 = open('func/parus/sql/covid_54_error.sql', 'r').read()
    SQL_3 = open('func/parus/sql/covid_54_2_svod.sql', 'r').read()

    DF_1 = parus_sql(SQL_1) 

    #ERROR = parus_sql(SQL_2)

    DF_2 = parus_sql(SQL_3)

    DATE_1 = DF_1.at[0,'DAY']
    del DF_1['DAY']
    DATE_2 = DF_2.at[0,'DAY']
    del DF_2['DAY']

    NEW_NAME_1 = 'temp/54_COVID_19_'   + DATE_1 + '.xlsx'
    NEW_NAME_2 = 'temp/54_2_COVID_19_' + DATE_2 + '.xlsx'

    shutil.copyfile('help/54_COVID_19_svod.xlsx', NEW_NAME_1)
    shutil.copyfile('help/54_2_COVID_19_svod.xlsx', NEW_NAME_2)

    wb = openpyxl.load_workbook(NEW_NAME_1)
    ws = wb['svod']

    rows = dataframe_to_rows(DF_1,index=False, header=False)
    for r_idx, row in enumerate(rows,4):
        for c_idx, value in enumerate(row, 3):
            ws.cell(row=r_idx, column=c_idx, value=value)

    wb.save(NEW_NAME_1)

    wb = openpyxl.load_workbook(NEW_NAME_2)
    ws = wb['svod']

    rows = dataframe_to_rows(DF_2,index=False, header=False)
    for r_idx, row in enumerate(rows,3):
        for c_idx, value in enumerate(row, 2):
            ws.cell(row=r_idx, column=c_idx, value=value)

    wb.save(NEW_NAME_2)

    return NEW_NAME_1 + ';' + NEW_NAME_2


