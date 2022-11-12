

def isClass(objA, objB):
    """判断类型是否一致"""
    return type(objA) == type(objB)


def isList(obj):
    """判断是否是 列表"""
    return isinstance(obj, list)

def isDict(obj):
    return isinstance(obj, dict)


def compare(objA, objB):
    if not isClass(objA, objB): return False
    if not len(objA) == len(objB): return False


def compareObj(objA, objB, flag):
    if isList(objA):
        if not sorted(objA) == sorted(objB):
            "判断排序后是否一致"
            return False

    elif isDict(objA):
        pass

    else:
        pass

# import xlwings as xw
#
# app = xw.App(visible=False, add_book=False)
# app.display_alerts = False  # 警告关闭
# app.screen_updating = False  # 屏幕更新关闭

