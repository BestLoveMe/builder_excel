
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

local = 'dev'


space_dashboard_url = "https://api.huoban.com/v2/dashboard_group/space/{}/resource"
header = {'authority': 'api.huoban.com', 'accept': 'application/json', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'authorization': 'Bearer 3VCbYtqMUL5AfFmoXgtm2kXd9L7bGBvL8r0NkTgN001', 'cache-control': 'no-cache', 'cookie': 'visit_token=1666086009737; HUOBAN_SESSIONID=e80eb9f02024607a4469b9e2125103ff; access_token=3VCbYtqMUL5AfFmoXgtm2kXd9L7bGBvL8r0NkTgN001; user_id=3232861; HUOBAN_SESSIONID_BETA=3ee34a6e11bad53da5fe44f5eb9096bf; HUOBAN_AUTH_BETA=fd14fc9d550f020ce6e2d9e2d1121e54; HUOBAN_DATA_BETA=M3Gl48Puw6UVAhsc2EkL5b9WaepwnCgsoeIofBPDj7i5wNqUq5S57qW96C4bo4zRHMqjOUHumwviR8hVmPCo1Q%3D%3D; Hm_lvt_29e645b6615539290daae517d6a073c9=1666501049,1666580133,1666662114,1666748943; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%223232861%22%2C%22first_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22evoke_help%22%2C%22%24latest_utm_medium%22%3A%22embed%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgzZWE3NmYzZmQ0YjUtMDNlNjI3Nzg5NzI0NGZhLTcyNDIyZjJkLTIzMDQwMDAtMTgzZWE3NmYzZmUxMmUyIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzIzMjg2MSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%223232861%22%7D%2C%22%24device_id%22%3A%22183ea76f3fd4b5-03e6277897244fa-72422f2d-2304000-183ea76f3fe12e2%22%7D; Hm_lpvt_29e645b6615539290daae517d6a073c9=1666759883; HUOBAN_AUTH=e5a9d3d30d4beb48a308dcbce02847da; HUOBAN_DATA=3iXZLW6Uz1STNtRI3maSDbc%2BnHj5FxoiDzNNBoR%2BTPfJmV%2BCfqPrjL4pGqrbOYNpB8nrLuyRlOv3g00tMtH2Tg%3D%3D', 'origin': 'https://app.huoban.com', 'pragma': 'no-cache', 'referer': 'https://app.huoban.com/', 'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43', 'x-huoban-monitor-tag': 'dashboard_list', 'x-huoban-return-fields': '["dashboard_id", "name", "rights", "ref_type", "ref_id", "last_sync_on", "alias"]', 'x-huoban-security-token': '', 'x-huoban-sensors': '%7B%22visit_type%22%3A%22%E5%86%85%E9%83%A8%E7%B3%BB%E7%BB%9F%22%2C%22client_id%22%3A%221%22%2C%22platform_type%22%3A%22Web%E6%B5%8F%E8%A7%88%E5%99%A8%22%2C%22client_version%22%3A%22v4%22%2C%22is_register%22%3Atrue%2C%22env%22%3A%22prod%22%2C%22_distinct_id%22%3A%223232861%22%2C%22application_url%22%3A%22https%3A%2F%2Fapp.huoban.com%2Fspaces%2F11065%2Fdashboards%22%2C%22company_id%22%3A%2254%22%2C%22space_id%22%3A%2211065%22%7D'}

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

    with open(r'./widgets_class_list.pkl', 'rb') as f:
        # pickle.dump(widgets_class_list, f)

        widgets_class_list = pickle.load(f)
    with open(r'./check.txt', 'w') as f:
        for widget in widgets_class_list:
            try:
                widget_old = requests.post(url=widget.get_widget_url(), headers=header,json=widget.get_widget_data(),proxies=proxies).json()
                widget_new = requests.post(url=widget.get_widget_url(), headers=test05_header,json=widget.get_widget_data(),proxies=proxies).json()
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
    # check_data(request_widget_list(request_dashboard(4000000002948220)))
    check_data([])
    pass