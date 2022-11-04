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

    row = """curl 'https://api.huoban.com/paasapi/table/2100000008820386' \
  -H 'authority: api.huoban.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'authorization: Bearer Al8ZD9QRIH0wY5lTqnn2PsxjcXUMT2OhgmiQpG1L001' \
  -H 'cache-control: no-cache' \
  -H 'cookie: visit_token=1666086009737; HUOBAN_SESSIONID=e80eb9f02024607a4469b9e2125103ff; HUOBAN_SESSIONID_BETA=3ee34a6e11bad53da5fe44f5eb9096bf; HUOBAN_AUTH_BETA=fd14fc9d550f020ce6e2d9e2d1121e54; HUOBAN_DATA_BETA=M3Gl48Puw6UVAhsc2EkL5b9WaepwnCgsoeIofBPDj7i5wNqUq5S57qW96C4bo4zRHMqjOUHumwviR8hVmPCo1Q%3D%3D; access_token=Al8ZD9QRIH0wY5lTqnn2PsxjcXUMT2OhgmiQpG1L001; user_id=3232861; Hm_lvt_29e645b6615539290daae517d6a073c9=1666927185,1667184077,1667293818,1667353151; Hm_lpvt_29e645b6615539290daae517d6a073c9=1667353159; v5=1; canary_v5=always; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%223232861%22%2C%22first_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22evoke_help%22%2C%22%24latest_utm_medium%22%3A%22embed%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgzZWE3NmYzZmQ0YjUtMDNlNjI3Nzg5NzI0NGZhLTcyNDIyZjJkLTIzMDQwMDAtMTgzZWE3NmYzZmUxMmUyIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzIzMjg2MSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%223232861%22%7D%2C%22%24device_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%7D; HUOBAN_AUTH=bea256192b991a2e8295356d7d37c954; HUOBAN_DATA=B6%2BK3bSfoyCv8%2FC0cN1F9nf4ij2EXd24eWdQkmrlPTn7%2BcMhm6etKzyL05%2BHq4a1qTT0xa%2Fv3H2rzUy9%2Bjxrrw%3D%3D' \
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
  -H 'x-huoban-client-id: 1' \
  -H 'x-huoban-request-id: e05046cdc042798fbc983545910055e9' \
  -H 'x-huoban-security-token: ' \
  --compressed"""
    parse = CulParse(row)
    # parse.culParse(row)

    # print(parse.getUrl())
    print(parse.getHeader())
    # print(parse.getMethod())
    # print(parse.getData())
