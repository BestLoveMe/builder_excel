# -*- coding: utf-8 -*-
# @Time  : 2022/12/1 9:32
# @Author: 86136


import configparser
import json


class Config():
    def __init__(self, env=None):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='UTF-8')
        self.section = 'PRE'

        if env:
            self.set_env(env)

    def set_env(self, env):
        if env.upper() not in ['PRE', 'DEV', 'LOCAL']:
            raise ValueError("%s 参数没有在['PRE', 'DEV', 'LOCAL']范围中" % env)
        self.section = env.upper()

    def get_env_option(self, option):
        return self.config.get(section=self.section, option=option)

    def get_env_int_optin(self, option):
        return self.config.getint(section=self.section, option=option)

    def get_env_dict_optin(self, option):
        return json.loads(self.config.get(section=self.section, option=option))


    def set_option(self, option, value):
        self.config.set(section=self.section, option=option, value=value)
        self.config.write(open('config.ini', 'w'))


if __name__ == '__main__':
    c = Config()
    print(c.get_env_dict_optin('user'))
    c.set_option('name', '123')
