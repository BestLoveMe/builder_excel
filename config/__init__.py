# 配置文件
# 登录请求 authorization 认证参数
authorization = 'Bearer 3VCbYtqMUL5AfFmoXgtm2kXd9L7bGBvL8r0NkTgN001'



# local = "dev"
local = "pre"










from config.parameter_config import *
from config.url_config import *


if local == "dev":
    after_base_url = dev_after_base_url
else:
    after_base_url = pre_after_base_url