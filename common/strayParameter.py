
"""生成随机值"""
from faker import Faker
import datetime
import calendar
import random

import config

fake = Faker(locale='zh_CN')


def ean_parameter():
    """生成13位条形码"""
    return fake.ean13()

def ean_13parameter(length=13):
    """length 只能是 8 or 13"""
    return fake.ean(length=length)

def convertStrToDateTime(data_str, format):
    """将日期字符串 转换成datetime 日期对象
    eg:datetime.datetime.strptime('2022-10-22', '%Y-%m-%d')
    """
    return datetime.datetime.strptime(data_str, format)

def date_time_this_month_range():
    """返回当前月的 第一天和最后一天 的datetime"""
    tody = datetime.datetime.today()
    date_start = datetime.datetime(year=tody.year, month=tody.month, day=1)
    date_end = datetime.datetime(year=tody.year, month=tody.month, day=calendar.monthrange(tody.year, tody.month)[1])
    return date_start, date_end

def date_time_parameter(date_start_str=None, date_end_str=None):
    """
    随机返回两个日期之间 的日期时间;
    默认随机返回本月的日期时间
    可传入日期字符串 eg: 2022-10-22
    """
    date_start = date_time_this_month_range()[0] if date_start_str is None else convertStrToDateTime(date_start_str, config.str_to_date_format)
    date_end = date_time_this_month_range()[1] if date_start_str is None else convertStrToDateTime(date_end_str, config.str_to_date_format)
    return fake.date_time_between_dates(date_start, date_end)

def date_parameter(date_start=date_time_this_month_range()[0], date_end=date_time_this_month_range()[1], format=config.str_to_date_format):
    """
    随机返回两个日期之间 的日期;
    默认随机返回本月的日期
    可传入日期字符串 eg: 2022-10-22
    """
    if isinstance(date_start, str):
        date_start = convertStrToDateTime(date_start, format)
    if isinstance(date_end, str):
        date_end = convertStrToDateTime(date_end, format)
    return fake.date_between_dates(date_start, date_end)

def now_unix_time():
    """返回当前时间戳"""
    return int(datetime.datetime.now().timestamp())

def option_to_one(option:list):
    """传入列表，随机返回一个"""
    return random.choice(option)

def option_to_more(option:list, k=1):
    li = random.choices(option, k=k)
    l = []
    # 过滤一下重复值
    for i in li:
        if i not in l:
            l.append(i)
    return l

def richText_parameter():
    """返回一段话，富文本参数"""
    return fake.text(max_nb_chars=200, ext_word_list=None)

def textArea_text_parameter():
    """返回稍长一点，多行文本"""
    return fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)

def input_text_parameter():
    """返回一小句话，单行文本"""
    return fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)

def int_parameter(start_int=config.start_int, end_int=config.end_int):
    """返回随机整数
        可传入生成范围，否则按config中的范围生成
    """
    return random.randint(start_int, end_int)

def flot_parameter(start_int=config.start_int, end_int=config.end_int, precision=config.precision):
    """
    :param start_int: 生成小数的最小值
    :param end_int: 生成小数的最大值
    :param precision: 生成小数保留的小数位数
    :return: 返回随机小数
    """
    return round(random.uniform(start_int, end_int),precision)

def phone_number_parameter():
    """返回手机号"""
    return fake.phone_number()


if __name__ == '__main__':
    # print(text())
    # print(fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None) )
    print(option_to_more([1,2,3], k=1))
