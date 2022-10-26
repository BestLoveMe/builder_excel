

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

import json
rep = """[{"widget_id":2500000001849714,"type":"chart","values":{"total":0,"legend":[{"true_name":"\u6210\u7ee9(\u6c42\u548c)-rspli30z","name":"\u6210\u7ee9(\u6c42\u548c)"}],"compare_xAxis":{"type":"category","name":"\u5b66\u79d1","data":null},"xAxis":{"type":"category","name":"\u5b66\u79d1","data":[{"true_value":"\u5316\u5b66","value":"\u5316\u5b66","filter":{"and":[{"field":2200000135030290,"query":{"in":[2]}},{"field":2200000135514800,"query":{"em":false}},{"field":2200000135030291,"query":{"eq":"\u5316\u5b66"}}]}},{"true_value":"\u5386\u53f2","value":"\u5386\u53f2","filter":{"and":[{"field":2200000135030290,"query":{"in":[2]}},{"field":2200000135514800,"query":{"em":false}},{"field":2200000135030291,"query":{"eq":"\u5386\u53f2"}}]}},{"true_value":"\u5730\u7406","value":"\u5730\u7406","filter":{"and":[{"field":2200000135030290,"query":{"in":[2]}},{"field":2200000135514800,"query":{"em":false}},{"field":2200000135030291,"query":{"eq":"\u5730\u7406"}}]}},{"true_value":"\u6570\u5b66","value":"\u6570\u5b66","filter":{"and":[{"field":2200000135030290,"query":{"in":[2]}},{"field":2200000135514800,"query":{"em":false}},{"field":2200000135030291,"query":{"eq":"\u6570\u5b66"}}]}},{"true_value":"\u7269\u7406","value":"\u7269\u7406","filter":{"and":[{"field":2200000135030290,"query":{"in":[2]}},{"field":2200000135514800,"query":{"em":false}},{"field":2200000135030291,"query":{"eq":"\u7269\u7406"}}]}},{"true_value":"\u751f\u7269","value":"\u751f\u7269","filter":{"and":[{"field":2200000135030290,"query":{"in":[2]}},{"field":2200000135514800,"query":{"em":false}},{"field":2200000135030291,"query":{"eq":"\u751f\u7269"}}]}},{"true_value":"\u82f1\u8bed","value":"\u82f1\u8bed","filter":{"and":[{"field":2200000135030290,"query":{"in":[2]}},{"field":2200000135514800,"query":{"em":false}},{"field":2200000135030291,"query":{"eq":"\u82f1\u8bed"}}]}}]},"yAxis":{"type":"value","name":"\u6210\u7ee9"},"series":[{"is_compare_series":0,"field_key":"rspli30z","name":"\u6210\u7ee9(\u6c42\u548c)","true_name":"\u6210\u7ee9(\u6c42\u548c)-rspli30z","type":"line","data":["1590","1647","1669","1653","1763","1670","1715"]}]},"last_sync_on":"2022-06-21 14:04:11"}]"""
# j = json.loads(rep)
n = 1
s = '123'
print(hash(s))
d = {'a':234,'b':345}
t = {'a':234,'b':345}
print(hash(d))
print(hash(t))


