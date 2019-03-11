import requests


class SendMethod(object):
    """
    发送请求
    """

    def _send_get(self, url, data=None, **kwargs):
        """
        发送get请求
        :param url:  请求地址
        :param data:  请求参数 字典
        :param kwargs:  其它参数
        :return:  返回结果 字典
        """
        response = requests.get(url, params=data, **kwargs)
        return response.json()

    def _send_post(self, url, data=None, json=None, **kwargs):
        """
        发送post请求
        :param url:  请求地址
        :param data:  请求参数 字典
        :param json:  请求参数, 原生格式, 字典 变成 json
        :param kwargs: 其它参数
        :return: 返回响应结果 字典
        """
        response = requests.post(url, data=data, json=json, **kwargs)
        return response.json()

    def _send_put(self, url, data=None, json=None, **kwargs):
        """
        发送put请求
        :param url: 请求地址
        :param data:  请求数据 dict
        :param json:  请求数据 dict 转换json
        :param kwargs:  其它数据
        :return:  返回响应结果
        """
        response = requests.put(url=url, data=data, json=json, **kwargs)
        return response.json()

    # 封装delete
    def _send_delete(self, url, data=None, **kwargs):
        """
        完成delete的请求
        :param url:  请求地址
        :param data:  请求数据
        :return: 状态码
        """
        response = requests.delete(url=url, params=data, **kwargs)
        return response.status_code

    def send_main(self, method, url, data=None, json=None, **kwargs):
        """只用调用该方法,完成所有的请求"""
        if method == "get":
            res = self._send_get(url=url, data=data, **kwargs)
        elif method == "post":
            res = self._send_post(url=url, data=data, json=json, **kwargs)
        elif method == "put":
            res = self._send_put(url=url, data=data, json=json, **kwargs)
        elif method == "delete":
            res = self._send_delete(url=url, data=data, **kwargs)
        else:
            res = None
        # 返回结果
        return res


if __name__ == '__main__':
    send = SendMethod()
    # url = "http://127.0.0.1:8000/api/departments/"
    # res = send.send_main("get",url=url)
    # print(res)

    url = "http://127.0.0.1:8000/api/departments/"
    data = {
        "data": [
            {
                "dep_id": "T02",
                "dep_name": "Test学院",
                "master_name": "Test-Master",
                "slogan": "Here is Slogan"
            }
        ]
    }
    res = send.send_main("post",url=url,json=data)
    print(res)
