

class Item():
    def __init__(self, item_list=None):
        self.item_id = None
        self.created_on = None
        self.created_by = None
        self.updated_on = None
        self.updated_by = None
        self.last_acticity_on = None

        self.rights = []
        self.fields = []


    def itemParse(self, fields, item, users):
        """"""
        """
        :param fields: 表格的 所有fields 对象集合
        :param item: item_lsit 的一条 item 的 值列表
        :param users: item_list mapping 中的 users 集合
        :return: 
        """
        self.item_id = item[0]
        for field in fields:
            if isinstance(field, BaseUser):
                field.setUserMapping(users)
            field.setValue(item[field.getIndex()])
        self.fields = fields





if __name__ == '__main__':
    pass
