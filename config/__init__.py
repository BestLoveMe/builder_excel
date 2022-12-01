# 配置文件

from .path import *


# local = "dev"
# local = "pre"
local = 'local'




def __getattr__(name):
    return 'config'

def __getattribute__(item):
    return "__getattribute__"

from config.parameter_config import *
from config.url_config import *

if local == "dev":
    after_base_url = dev_after_base_url
    user = dev_user
elif local == "pre":
    after_base_url = pre_after_base_url
    user = pre_user
elif local == "local":
    after_base_url = local_after_base_url
    user = local_user




