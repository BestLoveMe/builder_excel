# 配置文件
# 登录请求 authorization 认证参数
authorization = 'Bearer 3VCbYtqMUL5AfFmoXgtm2kXd9L7bGBvL8r0NkTgN001'



# local = "dev"
# local = "pre"
local = 'local'











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
