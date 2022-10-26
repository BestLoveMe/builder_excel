import json
import re

# 解析cCUL bash, 分解 url， header， data， 判断 method
class CulParse(object):
    def __init__(self, cur_bash=None):
        self._url = None
        self._header = None
        self._data = None
        self._method = None


        self._url_pattern = r'curl \'(\S*)\''
        self._header_pattern = r'-H \'(\S*[\s\S]*?)\''
        self._data_pattern = r'--data-(raw|binary){1} \'(.*)\''
        self._method_pattern = r'-X \'(\S*)\''

        if cur_bash != None:
            self.culParse(cur_bash)

    def getUrl(self):
        return self._url

    def getHeader(self):
        return self._header

    def getData(self):
        return self._data

    def getMethod(self):
        return self._method.lower() if self._method is not None else None

    def culParse(self, cur_bash):
        """传入 cul_bash 解析分解"""
        url = re.match(self._url_pattern, cur_bash)
        self._url = url.group(1) if url else None

        headers = re.findall(self._header_pattern, cur_bash)
        self._header = dict(h.split(': ') for h in headers) if headers else None

        content_type = self._header.get("content-type", None)
        if content_type is None:
            content_type = self._header.get("Content-Type", None)

        bodys = re.search(self._data_pattern, cur_bash)

        # 若请求头中 content_type 含有json, 则 data 解析成 dict， 否则 data 等于 解析出的字符串
        self._data = bodys.group(2) if bodys else None
        if (content_type is not None) and (re.search(r'json', content_type)):
            self._data = json.loads(bodys.group(2)) if bodys else None

        # 判断method， 若 bash 解析出 method，则为解析的请求方式; 否则判断data是否为空，为空是GET 请求；data不为空 为POST请求
        method = re.search(self._method_pattern, cur_bash)
        if method:
            self._method = method.group(1)
        elif self._data is None:
            self._method = "GET"
        else:
            self._method = "POST"


if __name__ == '__main__':

    row = """curl 'https://api.huobandev.com/paasapi/dashboard/2400000000483091/get_widget_value' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Authorization: Bearer LdGwot7GDw7qufu0T0ULSqp1zSnCrO0ZOQkyjr77001' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: hb_dev_host=test05; access_token=8syynUH1t8PQmqhUWLHRHkxsYa63Olgx1MxBtY1I012; user_id=1376905; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221369928%22%2C%22first_id%22%3A%2218381f97f20b41-077a6a9d2e908a4-26021a51-2304000-18381f97f21d22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiIxMzY5OTI4IiwiJGlkZW50aXR5X2Nvb2tpZV9pZCI6IjE4MzgxZjk3ZjIwYjQxLTA3N2E2YTlkMmU5MDhhNC0yNjAyMWE1MS0yMzA0MDAwLTE4MzgxZjk3ZjIxZDIyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221369928%22%7D%2C%22%24device_id%22%3A%2218381f97f20b41-077a6a9d2e908a4-26021a51-2304000-18381f97f21d22%22%7D' \
  -H 'Origin: https://app-03.huobandev.com' \
  -H 'Pragma: no-cache' \
  -H 'Referer: https://app-03.huobandev.com/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' \
  -H 'X-Huoban-Request-Id: a8e0ab3aa866bbc81683e58eb0fb3fa0' \
  -H 'X-Huoban-Security-Token: ' \
  -H 'sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --data-raw '{"widgets":[{"widget_id":2500000001849765,"ext_filter":1,"filter":{"and":[]}}]}' \
  --compressed"""
    parse = CulParse(row)
    # parse.culParse(row)

    # print(parse.getUrl())
    print(parse.getHeader())
    # print(parse.getMethod())
    # print(parse.getData())
