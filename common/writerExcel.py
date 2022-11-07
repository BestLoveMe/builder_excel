import pandas as pd
from collections import defaultdict

import config
from infoObject.table import Table
import xlwings as xw
from common.strayParameter import now_unix_time

def total(func):
    def total_time(*args, **kwargs):
        start_time = timer()
        func(*args, **kwargs)
        end_tiem = timer() - start_time
        print(end_tiem)
    return total_time


def to_csv(row):
    da = defaultdict(list)
    fields_list = Table(2100000020573043).get_writer_fields_list()

    for field in fields_list:
        for _ in range(row):
            da[field.getFieldId()].append(field.get_random_value())

    df = pd.DataFrame(da)

    df.to_csv(r'./data.csv')

@total
def toxls(table_id, row):
    table = Table(table_id)
    fields_list = list(table.get_writer_fields_list())
    name = [field.getName() for field in fields_list]
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False  # 警告关闭
    app.screen_updating = False  # 屏幕更新关闭
    wb = app.books.add()
    sheet = wb.sheets.active
    # 横向写入名称
    sheet.range("A1:A%d" % (len(name) + 1)).value = name
    # 纵向写入内容
    for index, field in enumerate(fields_list):
        # 纵向写入数据
        sheet.range((2, index + 1)).options(transpose=True).value = [field.get_random_value() for _ in range(row)]

    wb.save(config.FILE_DIR+ r'\{}-{}.xlsx'.format(table.name, now_unix_time()))
    wb.close()
    app.quit()

@total
def toxlsx2(table_id, row):
    table = Table(table_id=table_id)
    fields_list = list(table.get_writer_fields_list())
    name = [field.getName() for field in fields_list]
    da = []

    # 生成名称行
    da.append([field.getName() for field in fields_list])

    # 生成数据行
    for _ in range(row):
        l = []
        for field in fields_list:
            l.append(field.get_random_value())
        da.append(l)

    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False  # 警告关闭
    app.screen_updating = False  # 屏幕更新关闭
    wb = app.books.add()
    sheet = wb.sheets.active
    sheet.range('A1').value = da

    wb.save(config.FILE_DIR+r'\{}-{}.xlsx'.format(table.name, now_unix_time()))
    wb.close()
    app.quit()


import time

timer = time.time


if __name__ == '__main__':
    # to_csv(10)
    toxls(2100000001000050, 10000)
    """6.284190654754639"""
