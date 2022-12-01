

from infoObject.fieldtype.field import *


class FieldFunction():
    @staticmethod
    def map_func(map, key, configuration):
        obj = map.get(key)()
        obj.setConfiguration(configuration)
        return obj

    @staticmethod
    def text_function(configuration):
        text_map = {"input":InputTextField,
                    "textarea":TextareaTextField,
                    "rich":RichTextField,
                    "number":NumberTextField,
                    "barcode":BarcodeTextField
                    }
        field_type = configuration.get('config').get('sub_type')
        if field_type is None:
            field_type = configuration.get('config').get('type')
        return FieldFunction.map_func(text_map, field_type, configuration)

    @staticmethod
    def num_function(configuration):
        num_map = {'number':NumberField,
                   'percent':PercentField}
        field_type = configuration.get('config').get('display_mode')
        return FieldFunction.map_func(num_map, field_type, configuration)

    @staticmethod
    def calculation_function(configuration):
        cal_map = {'number':CalculationNumber,
                   'percent':CalculationPercent,
                   'date':CalculationDate,
                   'datetime':CalculationDateTime}
        field_type = configuration.get('config').get('display_mode')
        return FieldFunction.map_func(cal_map, field_type, configuration)

    @staticmethod
    def date_function(configuration):
        date_map = {'date':DateField,
                    'datetime':DateTimeField}
        field_type = configuration.get('config').get('type')
        return FieldFunction.map_func(date_map, field_type, configuration)

    @staticmethod
    def category_function(configuration):
        cat_map = {'list':ListCategoryField,
                   'select':SelectCategoryField}
        field_type = configuration.get('config').get('display_mode')
        return FieldFunction.map_func(cat_map, field_type, configuration)


    @staticmethod
    def user_function(configuration):
        user = UserFiled()
        user.setConfiguration(configuration)
        return user

    @staticmethod
    def relation_function(configuration):
        relation = RelationFieldField()
        relation.setConfiguration(configuration)
        return relation

    @staticmethod
    def location_function(configuration):
        local = SpecLocationField()
        local.setConfiguration(configuration)
        return local

    @staticmethod
    def file_function(configuration):
        file_map = {'image':ImageField,
                    'file':FileField,
                    'signature':SignatureField}
        field_type = configuration.get('type')
        return FieldFunction.map_func(file_map, field_type, configuration)


    @staticmethod
    def initField(configuration):
        """  判断field  的type类型，分发 调用不同的 field对象工厂函数，生成对应的 对象 并返回"""
        fieldType = configuration.get('type')
        mp = {'text':'text_function',
              'number':'num_function',
              'calculation':'calculation_function',
              'date':'date_function',
              'category':'category_function',
              'user':'user_function',
              'relation':'relation_function',
              'location':'location_function',
              'image':'file_function',
              'file':'file_function',
              'signature':'file_function'}
        map_func_str = mp.get(fieldType)
        if map_func_str:
            f = getattr(FieldFunction, map_func_str)

            return f(configuration)
        return None