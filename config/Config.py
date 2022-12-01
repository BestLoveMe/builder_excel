# -*- coding: utf-8 -*-
# @Time  : 2022/12/1 9:32
# @Author: 86136


import configparser



class Config():
    def __init__(self, env=None, ):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='UTF-8')
        self.section = 'PRE'


    def get_even_option(self, option):

        return self.config.get(section=self.section, option=option)




if __name__ == '__main__':
    c = Config()
    print(c.get_even_option('str_to_datetime_format'))