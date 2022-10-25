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

    row = """curl 'https://api.huobandev.com/paas/hbdata/item/item_list' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Authorization: Bearer HAvBxMy1NlrjKi74rBi9bEafilrPDmCp7qXKGsgg001' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: hb_dev_host=test08; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221370215%22%2C%22first_id%22%3A%22181db9d481f98d-09e60382fc231e-1f343371-2304000-181db9d4820766%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22181db9d481f98d-09e60382fc231e-1f343371-2304000-181db9d4820766%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgxZGI5ZDliOWVlMzEtMDM1YThjNTM2ZmUxYThjLTFmMzQzMzcxLTIzMDQwMDAtMTgxZGI5ZDliOWYxMWY4IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTM3MDIxNSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221370215%22%7D%7D' \
  -H 'Origin: https://app-08.huobandev.com' \
  -H 'Pragma: no-cache' \
  -H 'Referer: https://app-08.huobandev.com/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --data-raw '{"offset":0,"limit":100,"permission_id":0,"filter":{},"search":{},"order_by":[{"sort":"desc","field":2200000137800892},{"sort":"asc","field":2200000137800894}],"search_connector":"","mode":"Service","table_id":2100000014305475}' \
  --compressed"""
    parse = CulParse(row)
    # parse.culParse(row)

    print(parse.getUrl())
    print(parse.getHeader())
    print(parse.getMethod())
    print(parse.getData())
