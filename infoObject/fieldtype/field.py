from infoObject.fieldtype.basefield import *
from common.strayParameter import *


def random_value_set_None(f):
    def wapper(*args, **kwargs):
        # if int_parameter(1,5) == 2:
        #     return None
        return f(*args, **kwargs)
    return wapper


class InputTextField(BaseTextField, RandomField):
    """单行文本"""

    # @random_value_set_None
    def get_random_value(self):

        return input_text_parameter()


class TextareaTextField(BaseTextField, RandomField):
    """多行文本"""

    @random_value_set_None
    def get_random_value(self):
        return textArea_text_parameter()


class RichTextField(BaseTextField, RandomField):
    """富文本"""

    @random_value_set_None
    def get_random_value(self):
        return richText_parameter()


class NumberTextField(BaseTextField, RandomField):
    """号码"""

    @random_value_set_None
    def get_random_value(self):
        return phone_number_parameter()


class BarcodeTextField(BaseTextField, RandomField):
    """条码"""

    @random_value_set_None
    def get_random_value(self):
        return ean_13parameter()


class NumberField(BaseNumField, RandomField):
    """数值"""

    @random_value_set_None
    def get_random_value(self):
        if self.precision is None or self.precision == "":
            precision = config.precision
        else:
            precision = int(self.precision)

        return flot_parameter(precision=precision)


class PercentField(BaseNumField, RandomField):
    """百分比"""

    @random_value_set_None
    def get_random_value(self):
        if self.precision is None or self.precision == "":
            precision = config.precision
        else:
            precision = int(self.precision)

        return flot_parameter(precision=precision)


class MoneyField(BaseNumField, RandomField):
    """金额"""

    @random_value_set_None
    def get_random_value(self):
        return flot_parameter(precision=self.precision)


class DateField(BaseDateField, RandomField):
    """日期字段"""

    @random_value_set_None
    def get_random_value(self):
        return date_parameter("2022-08-15", "2023-01-30")


class DateTimeField(BaseDateField, RandomField):
    """日期和时间字段"""

    @random_value_set_None
    def get_random_value(self):
        return date_time_parameter("2022-08-15", "2023-01-30")


class CalculationNumber(BaseCalculationField, BaseNumField):
    """计算数值"""
    pass


class CalculationPercent(BaseCalculationField, BaseNumField):
    """计算百分比"""
    pass


class CalculationDate(BaseCalculationField, BaseDateField):
    """计算日期"""
    pass


class CalculationDateTime(BaseCalculationField, BaseDateField):
    """计算日期和时间"""
    pass


class ListCategoryField(BaseOptionField, RandomField):
    """选项字段类型"""

    @random_value_set_None
    def get_random_value(self):
        if self.options:
            # single类型是单选；multi 是多选
            if self.data_type == 'single':
                return option_to_one([o.get('name') for o in self.options])
            elif self.data_type == 'multi':
                return ','.join(
                    option_to_more([o.get('name') for o in self.options], k=int_parameter(0, len(self.options))))


class SelectCategoryField(BaseOptionField, RandomField):
    """下拉菜单"""

    @random_value_set_None
    def get_random_value(self):
        if self.options:
            # single类型是单选；multi 是多选
            if self.data_type == 'single':
                return option_to_one([o.get('name') for o in self.options])
            elif self.data_type == 'multi':
                return ','.join(
                    option_to_more([o.get('name') for o in self.options], k=int_parameter(0, len(self.options))))


class UserFiled(BaseUserField, RandomField):
    """成员字段"""

    @random_value_set_None
    def get_random_value(self):
        user_list = self._get_user_list()
        # if user_list and config.local != "local":
        #     """缩小一下 成员可选的范围"""
        #     user_list = [user for user in user_list if user.get('name') in ('侯真杰', '孙长子', '朱鲁迪', '宋培琳', '孙先菊')]
        if user_list:
            # single类型是单选；multi 是多选
            if self.data_type == 'single':
                return option_to_one(user_list).get('name')
            elif self.data_type == 'multi':
                return ','.join(user.get('name') for user in option_to_more(user_list, k=int_parameter(0, len(user_list))))


class RelationFieldField(BaseRelationField, RandomField):
    """关联字段"""

    @random_value_set_None
    def get_random_value(self):
        relation_items = self._get_relation_item_list()
        if self.data_type == 'single':
            return option_to_one(relation_items).get('title')
        if self.data_type == 'multi':
            return ','.join(
                item.get('title') for item in option_to_more(relation_items, k=int_parameter(0, len(relation_items))))


class SpecLocationField(BaseLocationField):
    """位置字段"""
    pass


class FileField(BaseFileField):
    """附件"""
    pass


class ImageField(BaseFileField):
    pass


class SignatureField(BaseFileField):
    """手写签名"""
    pass


if __name__ == '__main__':
    field = InputTextField()
    print(field.get_random_value())