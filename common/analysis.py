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

    row = """curl 'https://api.huoban.com/v2/dashboard/2400000001069234/get_widget_value' \
  -H 'authority: api.huoban.com' \
  -H 'accept: application/json' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'authorization: Bearer 8O5B4Pjl9FwsGISuawHWkImuN6uEyK6AXrhd6mgq001' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'cookie: visit_token=1663924904144; HUOBAN_SESSIONID=676bdd1b75be0d1e02cb5a8f96512266; HUOBAN_SESSIONID_BETA=9f3ad75c0e9e4e9571a28feebcb6d831; user_id=4360620; access_token=8O5B4Pjl9FwsGISuawHWkImuN6uEyK6AXrhd6mgq001; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%222640551%22%2C%22first_id%22%3A%2218369a71ebb42c-07085b9586c70a8-26021a51-2304000-18369a71ebc1038%22%2C%22props%22%3A%7B%22%24latest_utm_source%22%3A%22evoke_help%22%2C%22%24latest_utm_medium%22%3A%22embed%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgzNjlhNzFlYmI0MmMtMDcwODViOTU4NmM3MGE4LTI2MDIxYTUxLTIzMDQwMDAtMTgzNjlhNzFlYmMxMDM4IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMjY0MDU1MSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%222640551%22%7D%2C%22%24device_id%22%3A%2218369a71ebb42c-07085b9586c70a8-26021a51-2304000-18369a71ebc1038%22%7D; HUOBAN_AUTH_BETA=7148fce3bf2e5347dd1d564e2294308f; HUOBAN_DATA_BETA=PgYU%2BglyORaYRYIp3BTy5RiqL90dSprxrp8xvsyj6LL3P36TtRhJMyDh5FDx4BIvid6el2htsHbeDfCOmYf5GA%3D%3D; Hm_lvt_29e645b6615539290daae517d6a073c9=1666924615,1666939608,1667212371,1667268182; Hm_lpvt_29e645b6615539290daae517d6a073c9=1667268182; HUOBAN_AUTH=58b58528402770768c661bbe6e908796; HUOBAN_DATA=M9SzKQBLMG0JP7Eo6htlDGXvZldTpY2VqSvWB8NeFB0lzuw7EDlhHVaxy%2FYJu6TgEonx2w5kd4z8KJmZ6sF4UsvrEFw8tKeqbmlr9K3Y%2B0OiXmoE1XY5umCUT5MlyeQDPd1VgLNO1wzStPt6u4euxBWVMpuabRjfm4QmLZQS%2F%2BQ%3D' \
  -H 'origin: https://app.huoban.com' \
  -H 'pragma: no-cache' \
  -H 'referer: https://app.huoban.com/' \
  -H 'sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' \
  -H 'x-huoban-monitor-tag: dashboard_update' \
  -H 'x-huoban-security-token: ' \
  -H 'x-huoban-sensors: %7B%22visit_type%22%3A%22%E5%86%85%E9%83%A8%E7%B3%BB%E7%BB%9F%22%2C%22client_id%22%3A%221%22%2C%22platform_type%22%3A%22Web%E6%B5%8F%E8%A7%88%E5%99%A8%22%2C%22client_version%22%3A%22v4%22%2C%22is_register%22%3Atrue%2C%22env%22%3A%22prod%22%2C%22_distinct_id%22%3A%222640551%22%2C%22application_url%22%3A%22https%3A%2F%2Fapp.huoban.com%2Fspaces%2F4000000003433456%2Fdashboards%2F2400000001069234%22%2C%22company_id%22%3A%225100000000001643%22%2C%22space_id%22%3A%224000000003433456%22%7D' \
  --data-raw '{"widgets":[{"widget_id":2500000006975938,"name":"02表格图","description":"配置：图表：（1）有行、列分组，未勾选行总计，查看原始数据：普通用户：禁止查看，管理员：进入数据仓库；（2）样式：开启了分组折叠，列分组锁定，其他都没有设置"}]}' \
  --compressed"""
    parse = CulParse(row)
    # parse.culParse(row)

    # print(parse.getUrl())
    print(parse.getHeader())
    # print(parse.getMethod())
    # print(parse.getData())
