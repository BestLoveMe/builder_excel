import json
import re

# 解析cCUL bash, 分解 url， header， data， 判断 method
class CulParse(object):
    def __init__(self, cur_bash=None):
        self._url = None
        self._header = None
        self._data = None
        self._method = None

        self.__check_cul_pattern = r'^curl'
        self.__check_source_pattern = r'^curl --location'

        self.__browser_url_pattern = r'curl \'(\S*)\''
        self.__browser_header_pattern = r'-H \'(\S*[\s\S]*?)\''
        self.__browser_data_pattern = r'--data-(raw|binary){1} \'(.*)\''
        self.__browser_method_pattern = r'-X \'(\S*)\''


        self.__postman_method_pattern = r'curl --location --request (\S*)'
        self.__postman_url_pattern = r'curl(\s|\S)*?\'(\S*)\''
        self.__postman_header_pattern = r'-header \'(\S*[\s\S]*?)\''
        self.__postman_data_pattern = r'--data-(raw|binary){1} \'(.*)\''

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

    def __browser_bash_parse(self, cur_bash):
        """传入 浏览器的bash cul_bash 解析分解"""
        url = re.match(self.__browser_url_pattern, cur_bash)
        self._url = url.group(1) if url else None

        headers = re.findall(self.__browser_header_pattern, cur_bash)
        self._header = dict(h.split(': ') for h in headers) if headers else None

        content_type = None
        if isinstance(self._header, dict):
            content_type = self._header.get("Content-Type", None)

        bodys = re.search(self.__browser_data_pattern, cur_bash)

        # 若请求头中 content_type 含有json, 则 data 解析成 dict， 否则 data 等于 解析出的字符串
        self._data = bodys.group(2) if bodys else None
        if (content_type is not None) and (re.search(r'json', content_type)):
            self._data = json.loads(bodys.group(2)) if bodys else None

        # 判断method， 若 bash 解析出 method，则为解析的请求方式; 否则判断data是否为空，为空是GET 请求；data不为空 为POST请求
        method = re.search(self.__browser_method_pattern, cur_bash)
        if method:
            self._method = method.group(1)
        elif self._data is None:
            self._method = "GET"
        else:
            self._method = "POST"

    def __postman_bash_parse(self, cur_bash):
        # postmane 来源的bash解析
        method = re.match(self.__postman_method_pattern, cur_bash)
        self._method = method.group(1) if method else None

        url = re.match(self.__postman_url_pattern, cur_bash)
        self._url = url.group(2) if url else None

        headers = re.findall(self.__postman_header_pattern, cur_bash)
        self._header = dict(h.split(': ') for h in headers) if headers else None

        data = re.search(self.__postman_data_pattern, cur_bash)
        self._data = data.group(2) if data else None

        content_type = None
        if isinstance(self._header, dict):
            content_type = self._header.get("Content-Type", None)

        if self._data and content_type is not None and (re.search(r'json', content_type)):
            self._data = json.loads(self._data)


    def culParse(self, cur_bash):
        # 校验是否是 curl bash
        check = re.match(self.__check_cul_pattern, cur_bash)
        if not check:
            raise TypeError("cur_bash 格式错误")
        # 判断bash来源 是浏览器端，还是postman，并分别实现各自来源的解析
        source = re.match(self.__check_source_pattern, cur_bash)
        if source:
            self.__postman_bash_parse(cur_bash)
        else:
            self.__browser_bash_parse(cur_bash)


if __name__ == '__main__':

    row = """curl 'https://api.huobandev.com/v2/preference/table/2100000014467191' \
  -H 'Connection: keep-alive' \
  -H 'Pragma: no-cache' \
  -H 'Cache-Control: no-cache' \
  -H 'Accept: application/json' \
  -H 'X-Huoban-Request-Id: b150fdbaa7df80f958e7753a5f1412b2' \
  -H 'Authorization: Bearer 5kRW6YRQ2rOFGb0j7SdutQX3pFwMp8spd9ZizGgO001' \
  -H 'X-Huoban-Monitor-Tag: item_list' \
  -H 'X-Huoban-Client-Id: 1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' \
  -H 'X-Huoban-Sensors: %7B%22visit_type%22%3A%22%E5%86%85%E9%83%A8%E7%B3%BB%E7%BB%9F%22%2C%22client_id%22%3A%221%22%2C%22platform_type%22%3A%22Web%E6%B5%8F%E8%A7%88%E5%99%A8%22%2C%22client_version%22%3A%22v4%22%2C%22is_register%22%3Atrue%2C%22env%22%3A%22dev%22%2C%22_distinct_id%22%3A%221369930%22%2C%22application_url%22%3A%22https%3A%2F%2Fapp-06.huobandev.com%2Ftables%2F2100000014467191%3FviewId%3D3500000023666425%22%7D' \
  -H 'Origin: https://app-06.huobandev.com' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://app-06.huobandev.com/tables/2100000014467191?viewId=3500000023666425' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cookie: sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221369930%22%2C%22first_id%22%3A%221847f511fb5acd-061c5fcc4ef12e4-3e604809-1327104-1847f511fb896b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiIxMzY5OTMwIiwiJGlkZW50aXR5X2Nvb2tpZV9pZCI6IjE4NDdmNTExZmI1YWNkLTA2MWM1ZmNjNGVmMTJlNC0zZTYwNDgwOS0xMzI3MTA0LTE4NDdmNTExZmI4OTZiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221369930%22%7D%2C%22%24device_id%22%3A%221847f511fb5acd-061c5fcc4ef12e4-3e604809-1327104-1847f511fb896b%22%7D; user_id=1369930; hb_dev_host=test07; access_token=5kRW6YRQ2rOFGb0j7SdutQX3pFwMp8spd9ZizGgO001' \
  --compressed"""
    parse = CulParse(row)
    # parse.culParse(row)

    # print(parse.getUrl())
    print(parse.getHeader())
    # print(parse.getMethod())
    # print(parse.getData())
