import abc
import datetime

from common.SendRequest import sendRequest

def convertToDate(m):
    return datetime.datetime.utcfromtimestamp(int(m)).strftime("%Y-%m-%d")


def convertToDateTime(m):
    return datetime.datetime.utcfromtimestamp(int(m)).strftime("%Y-%m-%d %H:%M:%S")


class RandomField(abc.ABC):
    """生成随机值 的基类 """
    @abc.abstractmethod
    def get_random_value(self):
        """
        基类的 生成随机值的方法，
        继承此基类的字段，必须重写 该方法
        :return:
        """
        pass


class BaseField(object):
    range = {}
    mappings_fields = []
    def __init__(self):
        self.configuration = None # 整个字段的完整信息

        self.allow_create = None
        self.allow_lock = None
        self.allow_update = None
        self.attach_relation_field = None

        self.config = {} # 完整信息中的config
        self.default_setting = None # 默认配置，有默认参数
        self.description = None # 描述

        self.field_id = None
        self.name = None

        self.type = None
        self.data_type = None

        self.rights = []
        self.required = None  # 是否必填
        self.unique = None  # 是否唯一

        self.table_id = None  # table

        self.value = None
        self.index = None  # item_list 接口中字段映射的位置


    def setConfiguration(self, configuration):
        """
        :param configuration: 设置字段属性
        :return:
        """
        self.configuration = configuration
        for key in configuration:
            setattr(self, key, configuration.get(key))

        for key in self.config:
            attr = key
            if key == 'type':
                attr = 'data_type'
            setattr(self, attr, self.__getConfigType(key))

    def __getConfigType(self, t):
        """提取field 中config的信息"""
        return self.config.get(t)

    def getValue(self):
        return self.value

    def getRange(self, field_id):
        # 获取table
        if not BaseField.range:
            url = "https://api.huoban.com/paas/hbdata/field/filter/range"
            data = {"table_id":str(self.table_id)}
            try:
                BaseField.range = sendRequest.sendRequest('post', url=url, data=data)
            except Exception as e:
                pass
        if BaseField.range:
           for field in BaseField.range.get('data').get('fields'):
               if field.get('id') == field_id:
                    """{field_id: 2200000189561060,name: "单工作区成员",type: "user,values[{user_id:xxx, name:xxxx ...}]}"""
                    return field

    def getIndex(self):
        # 返回字段 在item_list 中映射的index
        if not self.index:
            for index, field_id in enumerate(BaseField.mappings_fields):
                if field_id == self.field_id:
                    self.index = index
                    return index
        return self.index

    def getName(self):
        return self.name

    def getFieldId(self):
        return self.field_id

class BaseTextField(BaseField):
    # 文本字段基类
    pass


class BaseNumField(BaseField):
    def __init__(self):
        super(BaseNumField, self).__init__()
        self.unit_name = None  # 单位
        self.display_mode = None  # 展示形式 number  percent
        self.precision = None  # 保留小数位
        self.separator = None  # 分隔符  "thousands", 千分位  ten-thousands 万分位
        self.unit_position = None  # 单位位置 "surfix", 后缀   prefix前缀

    def getValue(self):
        if self.value:
            value = self.__display_mode(self.value)
            value = self.__precision(value)
            value = self.__separator(value)
            value = self.__unit_position(value)
            return value
        return self.value

    def __display_mode(self, value):
        # num类型原值返回，百分比值乘以100返回
        if self.display_mode == 'number':
            return value
        elif self.display_mode == 'percent':
            return value * 100
        return value

    def __precision(self, value):
        # 保留小数处理
        if self.precision or self.precision == 0:
            fmt = '{:.%sf}' % self.precision
            return fmt.format(value)
        return value

    def __separator(self, value):
        # 分隔符处理
        if self.separator == 'thousands':
            return '{:,}'.format(value)
        elif self.separator == 'ten-thousands':
            return value
        return value

    def __unit_position(self, value):
        # 前后缀单位处理
        if self.display_mode == 'percent':
            self.unit_name = '%'
            self.unit_position = 'surfix'
        if self.unit_name:
            if self.unit_position == 'surfix':
                return '{}{}'.format(value, self.unit_name)
            else:
                return '{}{}'.format(self.unit_name, value)
        return value


class BaseDateField(BaseField):
    def getValue(self):
        if self.value:
            if self.data_type == 'date':
                return convertToDate(self.value)
            elif self.data_type == 'datetime':
                return convertToDateTime(self.value)
        return self.value


class BaseOptionField(BaseField):
    def __init__(self):
        super(BaseOptionField, self).__init__()
        self.options = []

    def getValue(self):
        if self.value and isinstance(self.value, list):
            return ','.join(o.get('name') for o in self.options if o.get('id') in self.value)


class BaseRelationField(BaseField):
    __item_list = []
    def __init__(self):
        super(BaseRelationField, self).__init__()
        self.__relation_items = None
        self.relation_field = [] # 本表的附加关联字段

    def getValue(self):
        if not self.__relation_items:
            url = 'https://api.huoban.com/paas/hbdata/item/batch_item_title'
            data = {"list":[{"table_id":"{}".format(self.table_id),"item_ids":[self.field_id]}]}
            try:
                self.__relation_items = sendRequest.sendRequest('post', url=url, data=data).get('data').get('list').get(int(self.field_id))
            except Exception as e:
                pass
        if self.__relation_items:
            return ','.join(item.get('title') for item in self.__relation_items)

    def _get_relation_item_list(self):
        # 获取当前关联字段的可选择的前 50条 item
        if not BaseRelationField.__item_list:
            url = 'https://api.huoban.com/paasapi/item/field/{}/search_relation'.format(self.field_id)
            data = {"text":"","offset":0,"limit":50,"table_id":self.table_id,"related_fields":{},"recommend_filter":{}}
            try:
                relation_json = sendRequest.sendRequest('post', url=url,  data=data)
                BaseRelationField.__item_list = relation_json
            except Exception as e:
                pass

        return BaseRelationField.__item_list


class BaseUserField(BaseField):
    __user_dict={}
    """成员基类"""
    def __init__(self):
        super(BaseUserField, self).__init__()
        self.option = []
        self.search = []


    def getVlue(self):
        values = self.getRange(self.field_id)
        if values and self.value:
            return ','.join(user.get('name') for user in values.get('values') if  user.get('user_id') if self.value)

    def _get_user_list(self):
        """返回 用户字段 请求的 sear_user 列表"""
        if not BaseUserField.__user_dict.get(self.field_id):
            url = 'https://api.huoban.com/paas/hbdata/field/{}/search_user'.format(self.field_id)
            data = {"text":"","offset":0,"limit":50,"table_id":self.table_id}
            user_list = None
            try:
                rep_json = sendRequest.sendRequest('post', url=url, data=data)
                user_list = rep_json.get('data').get('users')
            except Exception as e:
                pass
            if user_list:
                BaseUserField.__user_dict[self.field_id] = user_list

        return BaseUserField.__user_dict.get(self.field_id, [])



class BaseCalculationField(BaseField):
    """计算基类"""
    pass


class BaseLocationField(BaseField):
    """位置基类"""
    pass

class BaseFileField(BaseField):
    """文件基类"""
    pass










if __name__ == '__main__':
    option = BaseOptionField()
    option.options = [{'id': 1, 'name': 'xiao'}, {'id': 2, 'name': 'lll'}, {'id': 3, 'name': 'ppp'}]
    option.value = [1]
    print(option.getValue())
