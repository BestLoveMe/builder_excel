
from common.SendRequest import sendRequest
import config
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43', 'Accept-Encoding': 'gzip, deflate', 'accept': 'application/json', 'Connection': 'keep-alive', 'authority': 'api.huoban.com', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'authorization': 'Bearer 3VCbYtqMUL5AfFmoXgtm2kXd9L7bGBvL8r0NkTgN001', 'cache-control': 'no-cache', 'cookie': 'visit_token=1666086009737; HUOBAN_SESSIONID=e80eb9f02024607a4469b9e2125103ff; user_id=3232861; access_token=3VCbYtqMUL5AfFmoXgtm2kXd9L7bGBvL8r0NkTgN001; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%223232861%22%2C%22first_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22evoke_help%22%2C%22%24latest_utm_medium%22%3A%22embed%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgzZWE3NmYzZmQ0YjUtMDNlNjI3Nzg5NzI0NGZhLTcyNDIyZjJkLTIzMDQwMDAtMTgzZWE3NmYzZmUxMmUyIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzIzMjg2MSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%223232861%22%7D%2C%22%24device_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%7D; Hm_lvt_29e645b6615539290daae517d6a073c9=1666255593,1666317521,1666334889,1666417507; Hm_lpvt_29e645b6615539290daae517d6a073c9=1666417507; HUOBAN_AUTH=f5ec6ba88712dc21c64fc90033be04dd; HUOBAN_DATA=GQih9KhBlMj%2F9vhbyDf3bOiPcsmfaeiy96giTRi9ttg0KXtrrOvi9R34GwdqgeJ17o3kSKMox3DWcuzes2s2HA%3D%3D', 'origin': 'https://app.huoban.com', 'pragma': 'no-cache', 'referer': 'https://app.huoban.com/', 'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'x-huoban-monitor-tag': 'item_list', 'x-huoban-return-fields': '["*", "app_resource_setting", "exceptions", "procedure", {"space":["space_id", "name", "company_id"]}, "search_config"]', 'x-huoban-security-token': '', 'x-huoban-sensors': '%7B%22visit_type%22%3A%22%E5%86%85%E9%83%A8%E7%B3%BB%E7%BB%9F%22%2C%22client_id%22%3A%221%22%2C%22platform_type%22%3A%22Web%E6%B5%8F%E8%A7%88%E5%99%A8%22%2C%22client_version%22%3A%22v4%22%2C%22is_register%22%3Atrue%2C%22env%22%3A%22prod%22%2C%22_distinct_id%22%3A%223232861%22%2C%22application_url%22%3A%22https%3A%2F%2Fapp.huoban.com%2Ftables%2F2100000021121962%3FviewId%3D0%22%2C%22company_id%22%3A%225100000000001643%22%2C%22space_id%22%3A%224000000003745256%22%7D'}

class TableConfig():
    """
    请求获取table_config 的类，
    """
    def __init__(self, table_id):
        self.method = 'get'
        self.table_id = table_id
        self.url = 'https://api.huoban.com/paasapi/table/{}'.format(self.table_id)
        self.headers = headers

        self.headers['authorization'] = config.authorization

        self.__config = None

    def requestTableConfig(self):
        if self.__config is None:
            self.__config = sendRequest.sendRequest(self.method, url=self.url, headers=self.headers)
            if self.__config.get('code') is not None:
                raise PermissionError(self.__config.get('message'))
        return self.__config

    def getConfig(self):
        return self.requestTableConfig()


class ItemList(object):
    def __init__(self, table_id):
        self.url = 'https://api.huoban.com/paas/hbdata/item/item_list'
        self.data = {"offset":0,"limit":10000,"permission_id":0,"filter":{},"search":{},"order_by":[],"search_connector":"or","mode":"Client","table_id":table_id,"resource_view_type":"table"}
        self.methon = 'post'
        self.__item_list_json = None

    def __request_item_list(self):
        if self.__item_list_json is None:
            self.__item_list_json = sendRequest.sendRequest(self.methon, url=self.url, data=self.data)
            if self.__item_list_json.get('code') != 0:
                raise PermissionError(self.__item_list_json.get('message'))
        return self.__item_list_json

    def get_item_list_json(self):
        return self.__request_item_list()

    def get_item_list_items(self):
        return self.get_item_list_json().get('data').get('items')

    def get_item_list_mappings(self):
        return self.get_item_list_json().get('data').get('mappings')


if __name__ == '__main__':
    table = ItemList(2100000019084101)
    print(table.get_item_list_json())
    print(table.get_item_list_items())
    print(table.get_item_list_mappings())