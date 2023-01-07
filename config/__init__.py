# 配置文件


from config.ConfigParser import ConfigParser
from config.path import *
from config.parameter_config import *



class Config():
    def __init__(self):
        self.config = ConfigParser()
        self.local_env = "PRE"

    def set_enviroment(self, env:str):
        self.local_env = env.upper()
        self.config.set_env(env)

    @property
    def after_base_url(self):
        return self.config.get_env_option("base_api_url")

    @property
    def user(self):
        return self.config.get_env_dict_optin("user")

    @property
    def hb_dev_host(self):
        return "test05"

    @property
    def local(self):
        return self.local_env


configObject = Config()

if __name__ == '__main__':
    print(configObject.after_base_url)
