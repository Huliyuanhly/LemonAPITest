'''

'''
import json
import requests


class HandleRequest:
    '''
    处理请求
    '''

    def __init__(self):
        self.one_session = requests.Session()  # 创建会话对象，可以自动维护cookie

    def add_headers(self,  headers):
        '''
        添加公共请求头
        :param headers:
        :return:
        '''
        self.one_session.headers.update(headers)

    def send(self, url, method="post", data=None, is_json=True, **kwargs):
        #  data = '{"name":"huliyuan","gender":true}' json 格式的字符串
        #  data = "{'name':'huliyuan','gender':True}" 字典类型的字符串
        if isinstance(data, str):
            try:
                data = json.loads(data)  # 如果data是json类型的字符串，将它转换为Python中的数据类型
            except Exception as e:
                print("使用日志器来记录日志")
                data = eval(data)

        method = method.lower()
        if method == "get":
            # res = self.one_session,get(url,params=data,**kwargs)
            res = self.one_session.request(method, url, params=data, **kwargs)
        elif method in ("post", "put", "delete", "patch"):
            if is_json:  # 如果 is_json为True,那么使用json格式的形式来传参
                # res = self.one_session,post(url,params=data,**kwargs)
                res = self.one_session.request(method, url, json=data, **kwargs)
            else:
                # res = self.one_session,post(url,params=data,**kwargs)
                res = self.one_session.request(method, url, data=data, **kwargs)
        else:
            res = None
            print(f'不支持{method}请求方法')

        return res

    def close(self):
        self.one_session.close()


if __name__ == "__main__":
    # 1.构造请求的url
    login_url = "http://api.lemonban.com/futureloan/member/login"
    recharge_url = "http://api.lemonban.com/futureloan/member/recharge"
    # 2.创建请求参数
    headers = {
        "User-Agent": "Mozilla/5.0 huliyuan",
        "X-Lemonban-Media-Type": "lemonban.v2"
    }
    login_params = {
        "mobile_phone": "18244446667",
        "pwd": "12345678"
    }
    # 3.执行登录
    do_request = HandleRequest()  # 创建HandleRequest对象
    do_request.add_headers(headers)  # 添加公共请求头
    login_res = do_request.send(login_url, method="post", data=login_params, is_json=True)
    json_datas = login_res.json()
    member_id = json_datas['data']['id']
    token = json_datas['data']['token-info']['token']

    # 4.创建请求参数
    recharge_params = {
        "member_id": member_id,
        "amount": "5000"
    }

    token_header = {"Authorization": "Bearer" + token}
    do_request.add_headers(token_header)  # 从请求头中添加token
    # 5.执行充值
    recharge_res = do_request.send(recharge_url, data=recharge_params)
    pass
