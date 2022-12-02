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
        self.__browser_header_pattern = r'-H \'([\s\S]*?)\''
        self.__browser_data_pattern = r'--data-(raw|binary){1} \'(.*)\''
        self.__browser_method_pattern = r'-X \'(\S*)\''


        self.__postman_method_pattern = r'curl --location --request (\S*)'
        self.__postman_url_pattern = r'curl(\s|\S)*?\'(\S*)\''
        self.__postman_header_pattern = r'-header \'([\s\S]*?)\''
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
        print(headers)
        # self._header = dict((h.split(': ') for h in headers if ":" in h)) if headers else None
        # self._header = dict((h.split(': ') for h in headers if ":" in h)) if headers else None
        self._header = dict((re.split(r": |;", h, maxsplit=1)) for h in headers) if headers else None

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
        self._header = dict((re.split(r": |;", h, maxsplit=1)) for h in headers) if headers else None

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
    parse = CulParse(row)
    # parse.culParse(row)

    s = r'-H \'(\S*[\s\S]*?)\''

    # print(parse.getUrl())
    print(parse.getHeader())
    # print(parse.getMethod())
    print(parse.getData())
