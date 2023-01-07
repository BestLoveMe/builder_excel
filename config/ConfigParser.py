# -*- coding: utf-8 -*-
# @Time  : 2022/12/1 9:32
# @Author: 86136


import configparser
import json
from config.path import CONFIG_INI_FILE_PATH

class ConfigParser():
    def __init__(self, env=None):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_INI_FILE_PATH, encoding='UTF-8')
        self.section = 'PRE'

        if env:
            self.set_env(env)

    def set_env(self, env):
        """
        设置 config的环境
        """
        if env.upper() not in ['PRE', 'DEV', 'LOCAL']:
            raise ValueError("%s 参数没有在['PRE', 'DEV', 'LOCAL']范围中" % env)
        self.section = env.upper()

    def get_env_option(self, option):
        """
        获取 环境的 参数
        """
        return self.config.get(section=self.section, option=option)

    def get_env_int_optin(self, option):
        """
        返回 int类型的环境参数
        """
        return self.config.getint(section=self.section, option=option)

    def get_env_dict_optin(self, option):
        """
        返回将 参数转化成 字典返回
        """
        return json.loads(self.config.get(section=self.section, option=option))


    def set_option(self, option, value):
        """
        设置参数
        """
        self.config.set(section=self.section, option=option, value=value)
        self.config.write(open('config.ini', 'w'))


if __name__ == '__main__':
    c = ConfigParser()
    print(c.get_env_dict_optin('user'))
    print(c.get_env_option("base_api_url"))
    # c.set_option('name', '123')
