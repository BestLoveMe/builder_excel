import base64

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.models import Response
import execjs
import shelve

import config
from common.analysis import CulParse

# 取消 https 证书验证 的警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


headers_config = {'authority': 'api.huoban.com',
                  'accept': 'application/json, text/plain, */*',
                  'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                  'cache-control': 'no-cache','origin': 'https://app.huoban.com',
                  'pragma': 'no-cache',
                  'referer': 'https://app.huoban.com/',
                  'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
                  'sec-ch-ua-mobile': '?0',
                  'sec-ch-ua-platform': '"Windows"',
                  'sec-fetch-dest': 'empty',
                  'sec-fetch-mode': 'cors',
                  'sec-fetch-site': 'same-site',
                  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43',
                  'x-huoban-client-id': '1',
                  'x-huoban-request-id': 'e05046cdc042798fbc983545910055e9',
                  'x-huoban-security-token': ''}


class SendRequest(object):
    def __init__(self, cur_bash=None):
        self.r = CulParse(cur_bash)
        self.url = self.r.getUrl()
        self.method = self.r.getMethod()
        self.header = self.r.getHeader()
        self.data = self.r.getData()
        self.request = requests
        self.p = None


        # if cur_bash is not None:
        #     self.sendMethod()

    def sendMethod(self):
        # 从requests模块中获取 请求方法； 判断若获取到方法则 执行
        request = getattr(self.request, self.method)

        if request:
            self.p = request(url=self.url, headers=self.header, data=self.data, verify=False)

        return self.p

    def getResponseJson(self, row=None):
        """有 row 参数，重新初始化 self，发送请求，生成 response

            若响应中是 json格式 则获取json格式详情
            若响应不是json格式，则按文本获取 响应
        """

        if row:
            self.__init__(row)
        self.sendMethod()
        if isinstance(self.p, Response):
            if self.p.headers.get("content-type") == "application/json":
                try:
                    return self.p.json()
                except requests.exceptions.JSONDecodeError:
                    return self.p.text
            else:
                return self.p.text
        return self.p


class SimplePort():
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.__login()

        if config.local == "dev":
            self.__set_cookie_dev()

        self.retry = False
        self.__set_login_authorization()

    def _get_login_data(self):

        return {
            "username": config.user['username'],
            "password": config.user['pwd'],
            "grant_type": "password",
            "client_id": 1
        }
    def __set_cookie_dev(self):
        """cookie中设置dev环境中的 后端分支参数hb_dev_host"""
        cookie = self.session.cookies
        cookie.set("hb_dev_host", config.hb_dev_host)

    def __set_login_authorization(self):
        """添加请求头并设置 authorization 认证信息"""
        self.session.headers.update(headers_config)
        self.session.headers.update({'authorization':self.access_token})
        # self.session.headers.update({'authorization':"Bearer uPe4QoWSg4Ul7upJZjnt7z7d23eGWJSpTA5Ol1Es001"})


    def __login(self):
        """登录，获取 authorization"""
        modules_path = r"D:\Application\DevelopmentTool\node\node_global\node_modules\crypto-js"
        login_url = config.after_base_url + "/paasapi/login"
        access_token = self.sendRequest("post", login_url, data=self._get_login_data())
        # 判断登录是否成功
        if access_token.get('access_token'):
            access_token = access_token['access_token']
        else:
            print("用户名或密码错误")
            raise AttributeError
        with open(config.API_DIR + r"\get_authorization.js", 'r', encoding="utf-8") as f:
            js = f.read()

        token = base64.b64decode(access_token).decode()

        ctx = execjs.compile(js)
        result = ctx.call('get_token', token, modules_path)
        self.access_token = "Bearer " + result



    def sendRequest(self, method, url, headers=None, data=None):
        # 发送请求
        request = getattr(self.session, method.lower())
        if not request:
            raise PermissionError("{} 请求方法错误".format(method))
        p = request(url=url, headers=headers, json=data, verify=False)
        return self._getResponseJson(p)

    def _getResponseJson(self, response):
        """
            若响应中是 json格式 则获取json格式详情
            若响应不是json格式，则按文本获取 响应
        """
        if isinstance(response, Response):
            if response.headers.get("content-type") == "application/json":
                return response.json()
            else:
                d = response.text
                try:
                    response.json()
                except Exception as e:
                    pass
                else:
                    d = response.json()
                finally:
                    return d

        return response

    def sendRow(self, row):
        r = SendRequest(cur_bash=row)
        r.request = self.session
        return r.getResponseJson()


sendRequest = SimplePort()

if __name__ == '__main__':
    row = """curl 'https://api.huoban.com/v2/item/table/2100000017679108/import' \
  -H 'authority: api.huoban.com' \
  -H 'accept: application/json' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'authorization: Bearer WhU1SW6dnj7wvmVYteiMAFxuFclnttHBfKhZMYw9012' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'cookie: visit_token=1666086009737; HUOBAN_SESSIONID=88d6935c0f951427cc8836e2e323f256; user_id=3232861; Hm_lvt_29e645b6615539290daae517d6a073c9=1669686870,1669778057,1669862620,1669950422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%223232861%22%2C%22first_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22evoke_help%22%2C%22%24latest_utm_medium%22%3A%22embed%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiIzMjMyODYxIiwiJGlkZW50aXR5X2Nvb2tpZV9pZCI6IjE4M2VhNzZmM2ZkNGI1LTAzZTYyNzc4OTcyNDRmYS03MjQyMmYyZC0yMzA0MDAwLTE4M2VhNzZmM2ZlMTJlMiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%223232861%22%7D%2C%22%24device_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%7D; HUOBAN_SESSIONID_BETA=a3b5fd062b64ddf0c60a323cbbabca8d; HUOBAN_SYNC=2b0bFiXMpyDNZPIdP65DB%2BpaPAYKIl3o3REgLtc7PWONEv6scTaAWZIewReeU3gnvidnnkhK0%2BZJhQ; access_token=6HwWQVAruev5K3GHMkjc2GxsdqLWmmc8yFYVGydT001; Hm_lpvt_29e645b6615539290daae517d6a073c9=1669971151; v5=1; canary_v5=always; HUOBAN_AUTH_BETA=81248931637ee3c0f053ac7a424d1b79; HUOBAN_DATA_BETA=1A%2FahGBpdOqM0VllzkCNQ8aCiaN5f08KAoQop5sdK%2FuvhNuUm6D0dvlVPcBRN1cY%2FimwqECapAIU2qfGY0%2BeoQ%3D%3D; HUOBAN_AUTH=65ab7a7d52d2afa2836c1f08f277e31d; HUOBAN_DATA=Kc%2F3FKyLEzTtgB408K4wghs%2F0CRhvMJXt6yU9XpN1DpV5ArUynGC0omqWHcX%2Fgkrfuk7VkJYp9GeD265qgAGOg%3D%3D' \
  -H 'origin: https://app.huoban.com' \
  -H 'pragma: no-cache' \
  -H 'referer: https://app.huoban.com/' \
  -H 'sec-ch-ua: "Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43' \
  -H 'x-huoban-client-id: 1' \
  -H 'x-huoban-request-id: a80d7f51f5679485a6c82b6586614dfa' \
  -H 'x-huoban-security-token;' \
  -H 'x-huoban-sensors: %7B%22visit_type%22%3A%22%E5%86%85%E9%83%A8%E7%B3%BB%E7%BB%9F%22%2C%22client_id%22%3A%221%22%2C%22platform_type%22%3A%22Web%E6%B5%8F%E8%A7%88%E5%99%A8%22%2C%22client_version%22%3A%22v4%22%2C%22is_register%22%3Atrue%2C%22env%22%3A%22prod%22%2C%22_distinct_id%22%3A%223232861%22%2C%22application_url%22%3A%22https%3A%2F%2Fapp.huoban.com%2Ftables%2F2100000017679108%2Fimport%22%2C%22company_id%22%3A%225100000000001643%22%2C%22space_id%22%3A%224000000003480638%22%7D' \
  --data-raw '{"file_id":405750659,"type":"create","update_by":[],"mappings":[{"column_id":1,"field_id":2200000167480191},{"column_id":3,"field_id":2200000167480192},{"column_id":7,"field_id":2200000167480196},{"column_id":9,"field_id":2200000167480198},{"column_id":12,"field_id":2200000167480201}],"converter":{"title_row":1,"sheet":1,"delimiter":","},"from_import_table":false,"is_huge":false}' \
  --compressed"""

    # url = "https://www.baidu.com"
    # method = 'GET'
    # sendRequest.sendRequest(method, url)
    # print(sendRequest.session.headers)
    # print(sendRequest.session.cookies)
    print(SendRequest().getResponseJson(row))

    # sendRequest.login()
