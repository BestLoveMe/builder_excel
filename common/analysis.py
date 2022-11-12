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

    row = """curl 'https://devpress-api.csdn.net/api/internal/blog/nsInfo/blog/119924047' \
  -H 'authority: devpress-api.csdn.net' \
  -H 'accept: */*' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'cache-control: no-cache' \
  -H 'cookie: uuid_tt_dd=10_20293514760-1632185922881-928531; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_20293514760-1632185922881-928531; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%7D; c_dl_um=-; __gads=ID=e9bca87849074c41-22297f9779d700bd:T=1666539870:RT=1666539870:S=ALNI_MbwsbbWbKRii0sGP8lNpZ_IRRAyxg; __bid_n=18414f668492e9c71f4207; c_dl_prid=1664855552133_570253; c_dl_rid=1667020665951_564205; c_dl_fref=https://blog.csdn.net/csdncheng123/article/details/88294316; c_dl_fpage=/download/weixin_38668672/12855208; c_segment=3; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1667569325,1667622886,1667831485,1668225685; dc_sid=91bb73f862032052895ba5e66bbbf3c9; hide_login=1; __gpi=UID=0000059c972a0129:T=1653098673:RT=1668225684:S=ALNI_MapqbhfXH4BbyB0Ix7tzZLGgGg4NA; unlogin_scroll_step=1668225689164; SESSION=475b411b-4c6b-4867-8139-5b93ea5f5481; ssxmod_itna=iqjx2i0=dYqqz=QNexGwqWuPmTIqQuT9mxDsKONDSxGKidDqxBnuMGPDQNQgQOgjm0eirVYmqcGxopmQTNToy=x0aDbqGkGGGBxGGIxBYDQxAYDGDDpODj4ibDYSZHDjG96CSAPqAQDKx0kDY5Dwc58DYPDWxDFAcqbAPyaq9HhDi5Y2OGxAxG1DQ5Dsp2AgGKD0rfEgCHCk9oDE7+7xKYDvxDkY/FFP4GdLpyCsodNq74qql0tQ72YAD+xF0xTGiDuG0hxBm0PgW+x/mqx5QtP=vztDDPifkGDD; ssxmod_itna2=iqjx2i0=dYqqz=QNexGwqWuPmTIqQuTIxikpKFGDl2iiDj+qYC3dDQ0D6QWuj87HNqqFrT5=qj7jdT6pMbFlBiFWsUREU7KBm6oQdLjjwddRSbWLASn7kHZdXcRwuEQFqg9bHVtR3xnzfP7keFWNlPBaec+igxFGxheFQrOwTIetNKBzbgAttPAp8URzxcBzQcgtAFnE7E8praTKLmBfVi3FQFnUjzodT3SLCUEtLR4RM0eqoj4pd5BRgQ6pUF4Dw1u3DjKD+1wDD===; dc_session_id=10_1668231532733.768943; firstDie=1; log_Id_click=126; c_pref=default; c_ref=default; c_first_ref=default; log_Id_view=1090; c_first_page=https%3A//blog.csdn.net/m0_43609475/article/details/119924047; c_dsid=11_1668233314144.357102; c_page_id=default; dc_tos=rl812a; log_Id_pv=265; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1668233315' \
  -H 'origin: https://blog.csdn.net' \
  -H 'pragma: no-cache' \
  -H 'referer: https://blog.csdn.net/m0_43609475/article/details/119924047' \
  -H 'sec-ch-ua: ".Not/A)Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62' \
  --compressed"""
    parse = CulParse(row)
    # parse.culParse(row)

    print(parse.getUrl())
    print(parse.getHeader())
    print(parse.getMethod())
    print(parse.getData())
