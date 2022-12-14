
import requests
import pickle
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 取消 https 证书验证 的警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxies = {
    "http":"127.0.0.1:9393",
    "https":"127.0.0.1:9393"
}

local = 'pre'


space_dashboard_url = "https://api.huoban.com/v2/dashboard_group/space/{}/resource"
header = {'authority': 'api2.huoban.com', 'accept': 'application/json, text/plain, */*', 'accept-language': 'zh-CN,zh;q=0.9', 'authorization': 'Bearer 1x2t4qFczxRkyzQiqmYW3ToVedRFdil65oYvU5ci001', 'cache-control': 'no-cache', 'cookie': 'visit_token=1663924904144; HUOBAN_SESSIONID=676bdd1b75be0d1e02cb5a8f96512266; HUOBAN_SESSIONID_BETA=9f3ad75c0e9e4e9571a28feebcb6d831; Hm_lvt_29e645b6615539290daae517d6a073c9=1666924615,1666939608,1667212371,1667268182; Hm_lpvt_29e645b6615539290daae517d6a073c9=1667298903; v5=1; canary_v5=always; HUOBAN_AUTH_BETA=dece5333b61e8ac1ec540dc537054900; HUOBAN_DATA_BETA=0yRkPR1C%2F9Fs7Q5w0IbibGO5fj4%2B4A5owhc2ZjZWBqNTn3FQKs%2FxTd4hihU4xr7QpNg3sPlJqjQZvDRJOCaQzQ%3D%3D; HUOBAN_SYNC=d6d0dx3Fvk8wXab%2BLxX66OiosZMXhbFhxfi9kSyJ7ZXhQtpNWCkTwhHdXMexVCItu5YsY6PykqebAUckE%2FGdlsVU5suED2s%2FU5gtO0MEh8pOTFGdMAjYK8n9g8xXDoSzXNsbclHegR3xEg; access_token=1x2t4qFczxRkyzQiqmYW3ToVedRFdil65oYvU5ci001; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%222200242%22%2C%22first_id%22%3A%2218369a71ebb42c-07085b9586c70a8-26021a51-2304000-18369a71ebc1038%22%2C%22props%22%3A%7B%22%24latest_utm_source%22%3A%22evoke_help%22%2C%22%24latest_utm_medium%22%3A%22embed%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgzNjlhNzFlYmI0MmMtMDcwODViOTU4NmM3MGE4LTI2MDIxYTUxLTIzMDQwMDAtMTgzNjlhNzFlYmMxMDM4IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMjIwMDI0MiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%222200242%22%7D%2C%22%24device_id%22%3A%2218369a71ebb42c-07085b9586c70a8-26021a51-2304000-18369a71ebc1038%22%7D; HUOBAN_AUTH=ca84078205afcd7041a207faebb3c11c; HUOBAN_DATA=sLFXMYJ0Tc7xPL%2Fo%2Bo6v4b9k%2BxQTNWGjGDV9%2ByT5JtQPSGTnSIrVHi5xzHyZc7SCK%2BFOONfmtpqRy5eaIYlxigCGQQlF%2F5tq%2Bi7toE1SbyT619X8w%2BGZxM4HwZTMSX5TfmElyBSMvS6HwRRiSKgfwkcSqhvtRnjOKyE72tKGqWo%3D', 'origin': 'https://app.huoban.com', 'pragma': 'no-cache', 'referer': 'https://app.huoban.com/', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'x-huoban-client-id': '1', 'x-huoban-request-id': 'ad0ba3baeb3755943025588750e4b3d5', 'x-huoban-security-token': ''}

dashboard_url = "https://api.huoban.com/v2/dashboard/{}"
widget_url = "https://api.huoban.com/paasapi/dashboard/{}/get_widget_value"


test05_header = {'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Authorization': 'Bearer LdGwot7GDw7qufu0T0ULSqp1zSnCrO0ZOQkyjr77001', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Type': 'application/json;charset=UTF-8', 'Cookie': 'hb_dev_host=test05; access_token=8syynUH1t8PQmqhUWLHRHkxsYa63Olgx1MxBtY1I012; user_id=1376905; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221369928%22%2C%22first_id%22%3A%2218381f97f20b41-077a6a9d2e908a4-26021a51-2304000-18381f97f21d22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiIxMzY5OTI4IiwiJGlkZW50aXR5X2Nvb2tpZV9pZCI6IjE4MzgxZjk3ZjIwYjQxLTA3N2E2YTlkMmU5MDhhNC0yNjAyMWE1MS0yMzA0MDAwLTE4MzgxZjk3ZjIxZDIyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221369928%22%7D%2C%22%24device_id%22%3A%2218381f97f20b41-077a6a9d2e908a4-26021a51-2304000-18381f97f21d22%22%7D', 'Origin': 'https://app-03.huobandev.com', 'Pragma': 'no-cache', 'Referer': 'https://app-03.huobandev.com/', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'X-Huoban-Request-Id': 'a8e0ab3aa866bbc81683e58eb0fb3fa0', 'X-Huoban-Security-Token': '', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}

test08_header = {'Accept': 'application/json', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Authorization': 'Bearer KeqqmmYpECeYCuq3xpuhs3NE2B6zY0CYWH5wQeVx001', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Cookie': 'sajssdk_2015_cross_new_user=1; hb_dev_host=test08; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221369928%22%2C%22first_id%22%3A%2218412253a04e64-0707efb4b5c3758-26021a51-2304000-18412253a05f8b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiIxMzY5OTI4IiwiJGlkZW50aXR5X2Nvb2tpZV9pZCI6IjE4NDEyMjUzYTA0ZTY0LTA3MDdlZmI0YjVjMzc1OC0yNjAyMWE1MS0yMzA0MDAwLTE4NDEyMjUzYTA1ZjhiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221369928%22%7D%2C%22%24device_id%22%3A%2218412253a04e64-0707efb4b5c3758-26021a51-2304000-18412253a05f8b%22%7D', 'Origin': 'https://app-03.huobandev.com', 'Pragma': 'no-cache', 'Referer': 'https://app-03.huobandev.com/', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'X-Huoban-Monitor-Tag': 'dashboard_update', 'X-Huoban-Sensors': '%7B%22visit_type%22%3A%22%E5%86%85%E9%83%A8%E7%B3%BB%E7%BB%9F%22%2C%22client_id%22%3A%221%22%2C%22platform_type%22%3A%22Web%E6%B5%8F%E8%A7%88%E5%99%A8%22%2C%22client_version%22%3A%22v4%22%2C%22is_register%22%3Atrue%2C%22env%22%3A%22dev%22%2C%22_distinct_id%22%3A%221369928%22%2C%22application_url%22%3A%22https%3A%2F%2Fapp-03.huobandev.com%2Fspaces%2F4000000002948220%2Fdashboards%2F2400000000255635%22%2C%22company_id%22%3A%225100000000424303%22%2C%22space_id%22%3A%224000000002948220%22%7D', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}


if local == 'dev':
    dashboard_url = "https://api.huobandev.com/v2/dashboard/{}"
    space_dashboard_url = "https://api.huobandev.com/v2/dashboard_group/space/{}/resource"
    widget_url = "https://api.huobandev.com/v2/dashboard/{}/get_widget_value"
    header = test08_header


class Widget:
    """
    构建widget 图表组件类，保存相应的仪表盘和 图表信息
    """
    def __init__(self, dashboard_id, dashboard_name, widget_id, widget_name):
        self.dashboard_id = dashboard_id
        self.dashboard_name = dashboard_name
        self.widget_id = widget_id
        self.widget_name = widget_name
    def get_widget_url(self):
        """返回 请求图表的 URL"""
        return widget_url.format(self.dashboard_id)

    def get_widget_data(self):
        """返回 请求图表接口时 使用的参数"""
        return {"widgets":[{"widget_id":self.widget_id}]}

    def get_dashboard_url(self):
        """返回仪表盘 请求 图表组件的 api"""
        return dashboard_url.format(self.dashboard_id)

def request_dashboard(space_id):
    """
    返回工作区下的所有 仪表盘
    :param space_id: 工作区ID
    :return:
    """
    dashboard_list=[]
    try:
        res = requests.get(url=space_dashboard_url.format(space_id), headers=header, proxies=proxies).json()
    except Exception as e:
        print("dashboard失败：", space_id, space_dashboard_url.format(space_id))
        print(e)
    else:
        for da in res:
            """遍历 工作区下的所有 仪表盘，区分是否是分组，在分组中的，将分组中的也提取出来"""
            if da.get("type") == 'dashboard':
                dashboard_list.append(da)
            elif da.get('type') == "dashboard_group":
                dashboard_list.extend(da.get('dashboard_list'))

    return dashboard_list

def request_widget_list(dashboard_list):
    """遍历所有仪表盘请求 widget图表，组合成 widget 对象列表返回"""
    widgets_class_list = []
    for da in dashboard_list:
        dashboard_id = da.get('dashboard_id')
        dashboard_name = da.get('name')
        try:
            dashboard_res = requests.get(url=dashboard_url.format(dashboard_id), headers=header,proxies=proxies).json()
        except:
            print("失败：",dashboard_url)
        else:
            widgets_list = dashboard_res.get('widgets')
            for wi in widgets_list:
                # 过滤掉 筛选、流程-我处理的，快捷方式，流程-我发起的，
                if wi.get('type') not in ['filter','task','multi_shortcuts','process','single_shortcut']:
                    widgets_class_list.append(Widget(dashboard_id, dashboard_name,wi.get("widget_id"), wi.get("name")))

    return widgets_class_list


def check_data(widgets_class_list):
    """遍历 widget对象列表，请求两个分支的返回值，并进行比较，返回值不一致的 写入 txt文件中"""

    # with open(r'widgets_4000000003327788_list.pkl', 'wb') as f:
    #     pickle.dump(widgets_class_list, f)

        # widgets_class_list = pickle.load(f)
    print(widgets_class_list)
    with open(r'./check.txt', 'w') as f:
        for widget in widgets_class_list:
            try:
                widget_old = requests.post(url=widget.get_widget_url(), headers=header,json=widget.get_widget_data()).json()
                widget_new = requests.post(url=widget.get_widget_url(), headers=header,json=widget.get_widget_data(),proxies=proxies).json()
            except:
                print("失败：",widget.dashboard_name, widget.widget_id, widget.widget_name)
            else:
                if widget_old != widget_new:
                    print(widget.dashboard_name, widget.widget_id, widget.widget_name)
                    f.write('-----------------------------------------------------------------------------')
                    f.write(str(widget.dashboard_id))
                    f.write('\t')
                    f.write(str(widget.dashboard_name))
                    f.write('\t')
                    f.write(str(widget.widget_id))
                    f.write('\t')
                    f.write(str(widget.widget_name))
                    f.write('\n')
                    f.write(widget.get_widget_url())
                    f.write('\n')
                    f.write('原接口返回值：')
                    f.write('\n')
                    f.write(json.dumps(widget_old))
                    f.write('\n\n')
                    f.write('新接口返回值：')
                    f.write('\n')
                    f.write(json.dumps(widget_new))
                    f.write('\n\n\n\n')









if __name__ == '__main__':
    check_data(request_widget_list(request_dashboard(1785441)))
    # check_data([])
    pass