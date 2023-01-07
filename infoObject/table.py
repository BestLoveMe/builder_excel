import config
from infoObject.fieldFunction import FieldFunction
import collections

from connectorConfig.port import TableConfig
from infoObject.fieldtype.basefield import RandomField
from common.SendRequest import sendRequest

class Table(object):
    def __init__(self, table_id):
        self.items = []
        self.table_id = table_id
        self.procedure = {}
        self.space = {}
        self.rights = []
        self.fields_list = []
        self.system_fields = []
        self.item_list = []
        self.name = None

        self.tableConfig = TableConfig(self.table_id).getConfig()
        # self.table_config = self.__get_table_view_navigation_config()

        self.init_parse()

    def init_parse(self):
        """设置table 的基本信息"""
        # self.table_id = self.tableConfig.get("table_id")
        # self.procedure = self.tableConfig.get("procedure")
        # self.space = self.tableConfig.get("space")
        # self.rights = self.tableConfig.get("rights")

        for key in self.tableConfig:
            setattr(self, key, self.tableConfig.get(key))

        self.__parse_fields_list()


    def __parse_fields_list(self):
        """返回新的 field 对象 集合"""
        fields = self.tableConfig.get("fields")
        for configuration in fields:
            field_obj = FieldFunction.initField(configuration)
            if field_obj:
                self.fields_list.append(field_obj)

    def get_fields_list(self):
        return self.fields_list

    def get_writer_fields_list(self):
        """返回可以生成随机数的字段列表"""
        return (field for field in self.get_fields_list() if isinstance(field, RandomField) and not field.attach_relation_field)

    def __get_table_view_navigation_config(self):
        """
        请求获取 表格视图的 config
        """
        config_url = config.configObject.after_base_url + r"/paas/view/navigation/configs?table_id={}".format(self.table_id)
        return sendRequest.sendRequest('get', config_url)

    def get_table_views(self):
        """
        获取表格的 视图
        """
        def get_gourp_view(group):
            return group.get('children')
        views = collections.defaultdict(list)
        view_config_groups = self.table_config.get("view_config_groups")
        for views_group in view_config_groups:
            if views_group.get("scope") == "private":
                private_children = views_group.get("children")
                if private_children.get("type") == "group":
                    views["private"].extend(get_gourp_view(private_children))
                else:
                    views["private"].append(private_children)
            else:
                public_children = views_group.get("children")
                if public_children.get("type") == "group":
                    views["public"].extend(get_gourp_view(public_children))
                else:
                    views["public"].append(public_children)
        return views

    def delete_views(self):
        views = self.get_table_views()
        view_ids = []


if __name__ == '__main__':
    table = Table(2100000020573043)
    print(table.tableConfig)





