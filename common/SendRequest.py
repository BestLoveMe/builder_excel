import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.models import Response

import config
from common.analysis import CulParse

# 取消 https 证书验证 的警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers_config = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43',
    'Accept-Encoding': 'gzip, deflate', 'accept': 'application/json', 'Connection': 'keep-alive',
    'authority': 'api.huoban.com', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer 3VCbYtqMUL5AfFmoXgtm2kXd9L7bGBvL8r0NkTgN001', 'cache-control': 'no-cache',
    'cookie': 'visit_token=1666086009737; HUOBAN_SESSIONID=e80eb9f02024607a4469b9e2125103ff; user_id=3232861; access_token=3VCbYtqMUL5AfFmoXgtm2kXd9L7bGBvL8r0NkTgN001; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%223232861%22%2C%22first_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22evoke_help%22%2C%22%24latest_utm_medium%22%3A%22embed%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgzZWE3NmYzZmQ0YjUtMDNlNjI3Nzg5NzI0NGZhLTcyNDIyZjJkLTIzMDQwMDAtMTgzZWE3NmYzZmUxMmUyIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzIzMjg2MSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%223232861%22%7D%2C%22%24device_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%7D; Hm_lvt_29e645b6615539290daae517d6a073c9=1666255593,1666317521,1666334889,1666417507; Hm_lpvt_29e645b6615539290daae517d6a073c9=1666417507; HUOBAN_AUTH=f5ec6ba88712dc21c64fc90033be04dd; HUOBAN_DATA=GQih9KhBlMj%2F9vhbyDf3bOiPcsmfaeiy96giTRi9ttg0KXtrrOvi9R34GwdqgeJ17o3kSKMox3DWcuzes2s2HA%3D%3D',
    'origin': 'https://app.huoban.com', 'pragma': 'no-cache', 'referer': 'https://app.huoban.com/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"', 'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site', 'x-huoban-monitor-tag': 'item_list',
    'x-huoban-return-fields': '["*", "app_resource_setting", "exceptions", "procedure", {"space":["space_id", "name", "company_id"]}, "search_config"]',
    'x-huoban-security-token': '',
    'x-huoban-sensors': '%7B%22visit_type%22%3A%22%E5%86%85%E9%83%A8%E7%B3%BB%E7%BB%9F%22%2C%22client_id%22%3A%221%22%2C%22platform_type%22%3A%22Web%E6%B5%8F%E8%A7%88%E5%99%A8%22%2C%22client_version%22%3A%22v4%22%2C%22is_register%22%3Atrue%2C%22env%22%3A%22prod%22%2C%22_distinct_id%22%3A%223232861%22%2C%22application_url%22%3A%22https%3A%2F%2Fapp.huoban.com%2Ftables%2F2100000021121962%3FviewId%3D0%22%2C%22company_id%22%3A%225100000000001643%22%2C%22space_id%22%3A%224000000003745256%22%7D'}


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
        request = getattr(requests, self.method)
        if request:
            self.p = request(url=self.url, headers=self.header, json=self.data, verify=False)
        # if self.method == "GET":
        # self.p = requests.get(url=self.url, headers=self.header,verify=False)
        # elif self.method == "POST":
        #     p = requests.post(url=self.url, headers=self.header,json=self.data, verify=False)
        # elif self.method == "OPTIONS":
        #     p = requests.options(url=self.url, headers=self.header, verify=False)
        # elif self.method == "PUT":
        #     p = requests.put(url=self.url, headers=self.header, data=self.data, verify=False)
        # else:
        #     p = None
        # self.p = p
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
                return self.p.json()
            else:
                return self.p.text
        return self.p


class SimplePort():
    def __init__(self):
        self.session = requests.Session()

    def sendRequest(self, method, url, headers=None, data=None):
        if not headers:
            # 若没有传header，自行拼接 authorization 认证信息
            headers = headers_config
            headers['authorization'] = config.authorization
        # print("发送请求--", url)
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
                return response.text
        return response

    def sendRow(self, row):
        r = SendRequest(cur_bash=row)
        r.request = self.session
        return self._getResponseJson(r.sendMethod())


sendRequest = SimplePort()

if __name__ == '__main__':
    row = """curl 'https://api.huoban.com/v2/table/2100000021121962' \
  -H 'authority: api.huoban.com' \
  -H 'accept: application/json' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'authorization: Bearer 3VCbYtqMUL5AfFmoXgtm2kXd9L7bGBvL8r0NkTgN001' \
  -H 'cache-control: no-cache' \
  -H 'cookie: visit_token=1666086009737; HUOBAN_SESSIONID=e80eb9f02024607a4469b9e2125103ff; user_id=3232861; access_token=3VCbYtqMUL5AfFmoXgtm2kXd9L7bGBvL8r0NkTgN001; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%223232861%22%2C%22first_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22evoke_help%22%2C%22%24latest_utm_medium%22%3A%22embed%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgzZWE3NmYzZmQ0YjUtMDNlNjI3Nzg5NzI0NGZhLTcyNDIyZjJkLTIzMDQwMDAtMTgzZWE3NmYzZmUxMmUyIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzIzMjg2MSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%223232861%22%7D%2C%22%24device_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%7D; Hm_lvt_29e645b6615539290daae517d6a073c9=1666255593,1666317521,1666334889,1666417507; Hm_lpvt_29e645b6615539290daae517d6a073c9=1666417507; HUOBAN_AUTH=f5ec6ba88712dc21c64fc90033be04dd; HUOBAN_DATA=GQih9KhBlMj%2F9vhbyDf3bOiPcsmfaeiy96giTRi9ttg0KXtrrOvi9R34GwdqgeJ17o3kSKMox3DWcuzes2s2HA%3D%3D' \
  -H 'origin: https://app.huoban.com' \
  -H 'pragma: no-cache' \
  -H 'referer: https://app.huoban.com/' \
  -H 'sec-ch-ua: "Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43' \
  -H 'x-huoban-monitor-tag: item_list' \
  -H 'x-huoban-return-fields: ["*", "app_resource_setting", "exceptions", "procedure", {"space":["space_id", "name", "company_id"]}, "search_config"]' \
  -H 'x-huoban-security-token: ' \
  -H 'x-huoban-sensors: %7B%22visit_type%22%3A%22%E5%86%85%E9%83%A8%E7%B3%BB%E7%BB%9F%22%2C%22client_id%22%3A%221%22%2C%22platform_type%22%3A%22Web%E6%B5%8F%E8%A7%88%E5%99%A8%22%2C%22client_version%22%3A%22v4%22%2C%22is_register%22%3Atrue%2C%22env%22%3A%22prod%22%2C%22_distinct_id%22%3A%223232861%22%2C%22application_url%22%3A%22https%3A%2F%2Fapp.huoban.com%2Ftables%2F2100000021121962%3FviewId%3D0%22%2C%22company_id%22%3A%225100000000001643%22%2C%22space_id%22%3A%224000000003745256%22%7D' \
  --compressed"""

    # url = "https://www.baidu.com"
    # method = 'GET'
    # print(sendRequest.sendRequest(method, url))
    print(sendRequest.sendRow(row))
