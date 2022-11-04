
from common.SendRequest import sendRequest
import config



class TableConfig():
    """
    请求获取table_config 的类，
    """
    def __init__(self, table_id):
        self.method = 'get'
        self.table_id = table_id
        self.url = config.after_base_url+'/paasapi/table/{}'.format(self.table_id)

        self.__config = None

    def requestTableConfig(self):
        if self.__config is None:
            self.__config = sendRequest.sendRequest(self.method, url=self.url)
            if self.__config.get('code') is not None:
                raise PermissionError(self.__config.get('message'))
        return self.__config

    def getConfig(self):
        return self.requestTableConfig()


class ItemList(object):
    def __init__(self, table_id):
        self.url = config.after_base_url+ '/paas/hbdata/item/item_list'
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