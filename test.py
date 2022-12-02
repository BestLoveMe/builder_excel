import config
import re

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
s = "asdfa: 2w3wer:"
l = ['authority: api.huoban.com', 'accept: application/json', 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'authorization: Bearer WhU1SW6dnj7wvmVYteiMAFxuFclnttHBfKhZMYw9012', 'cache-control: no-cache', 'content-type: application/json', 'cookie: visit_token=1666086009737; HUOBAN_SESSIONID=88d6935c0f951427cc8836e2e323f256; user_id=3232861; Hm_lvt_29e645b6615539290daae517d6a073c9=1669686870,1669778057,1669862620,1669950422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%223232861%22%2C%22first_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22evoke_help%22%2C%22%24latest_utm_medium%22%3A%22embed%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiIzMjMyODYxIiwiJGlkZW50aXR5X2Nvb2tpZV9pZCI6IjE4M2VhNzZmM2ZkNGI1LTAzZTYyNzc4OTcyNDRmYS03MjQyMmYyZC0yMzA0MDAwLTE4M2VhNzZmM2ZlMTJlMiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%223232861%22%7D%2C%22%24device_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%7D; HUOBAN_SESSIONID_BETA=a3b5fd062b64ddf0c60a323cbbabca8d; HUOBAN_SYNC=2b0bFiXMpyDNZPIdP65DB%2BpaPAYKIl3o3REgLtc7PWONEv6scTaAWZIewReeU3gnvidnnkhK0%2BZJhQ; access_token=6HwWQVAruev5K3GHMkjc2GxsdqLWmmc8yFYVGydT001; Hm_lpvt_29e645b6615539290daae517d6a073c9=1669971151; v5=1; canary_v5=always; HUOBAN_AUTH_BETA=81248931637ee3c0f053ac7a424d1b79; HUOBAN_DATA_BETA=1A%2FahGBpdOqM0VllzkCNQ8aCiaN5f08KAoQop5sdK%2FuvhNuUm6D0dvlVPcBRN1cY%2FimwqECapAIU2qfGY0%2BeoQ%3D%3D; HUOBAN_AUTH=65ab7a7d52d2afa2836c1f08f277e31d; HUOBAN_DATA=Kc%2F3FKyLEzTtgB408K4wghs%2F0CRhvMJXt6yU9XpN1DpV5ArUynGC0omqWHcX%2Fgkrfuk7VkJYp9GeD265qgAGOg%3D%3D', 'origin: https://app.huoban.com', 'pragma: no-cache', 'referer: https://app.huoban.com/', 'sec-ch-ua: "Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile: ?0', 'sec-ch-ua-platform: "Windows"', 'sec-fetch-dest: empty', 'sec-fetch-mode: cors', 'sec-fetch-site: same-site', 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43', 'x-huoban-client-id: 1', 'x-huoban-request-id: a80d7f51f5679485a6c82b6586614dfa', 'x-huoban-security-token;', 'x-huoban-sensors: %7B%22visit_type%22%3A%22%E5%86%85%E9%83%A8%E7%B3%BB%E7%BB%9F%22%2C%22client_id%22%3A%221%22%2C%22platform_type%22%3A%22Web%E6%B5%8F%E8%A7%88%E5%99%A8%22%2C%22client_version%22%3A%22v4%22%2C%22is_register%22%3Atrue%2C%22env%22%3A%22prod%22%2C%22_distinct_id%22%3A%223232861%22%2C%22application_url%22%3A%22https%3A%2F%2Fapp.huoban.com%2Ftables%2F2100000017679108%2Fimport%22%2C%22company_id%22%3A%225100000000001643%22%2C%22space_id%22%3A%224000000003480638%22%7D']


if __name__ == '__main__':
    pass

    # for h in l:
    #     print(re.split(r": |;", h, ))

    d = dict((re.split(r": |;", h, maxsplit=1) for h in l))

    print(d)