from infoObject.fieldFunction import FieldFunction


from connectorConfig.port import TableConfig
from infoObject.fieldtype.basefield import RandomField

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


if __name__ == '__main__':
    table = Table(2100000020573043)
    for field in table.fields_list:
        if isinstance(field, RandomField):
            print()





