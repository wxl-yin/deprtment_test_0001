class GetKeywords(object):
    """
        自动帮我查找对应关键字的值
    """

    def get_keyword(self, data, keyword):
        """
        获取单个关键字对应的值
        :param data 数据源字典
        :keyword 关键字的名字
        :return:
        """
        if keyword in data.keys():  # 判断键是否在第一层
            return data[keyword]  # 如果存在就直接返回
        else:
            # 遍历
            for v in data.values():
                # 判断是字典还是列表
                if isinstance(v, list):  # 是列表
                    # 遍历列表
                    for item in v:
                        result = self.get_keyword(item,keyword)
                        # 判断是否获取到
                        if result or result == 0 or (result is not False and result is not None):
                            return result
                elif isinstance(v, dict):  # 是字典
                    result = self.get_keyword(v, keyword)
                    # 判断是否获取到
                    if result or result == 0 or (result is not False and result is not None):
                        return result

    def get_keywords(self, data, lebal, keyword):
        """
        根据关键字查询多个值
        :param data 数据源 字典
        :param lebal 对应关键字上层关键字
        :param keyword 关键字名字
        :return: list
        """
        # 对应lebal的值
        new_data = self.get_keyword(data,lebal)
        if isinstance(new_data,list):
            values = [] # 装数据
            for v in new_data:
                values.append(v[keyword])
            # 返回结果
            return values


if __name__ == '__main__':
    data = {
        "count": 0,
        "results": [
            {
                "username": "小三"
            },
            {
                "username": "李四"
            }
        ],
        "goods": [
            {
                "name": "肥皂",
                "status": [
                    {"status_name": "精品"},
                    {"status_name": "新品"}
                ]
            }
        ],
        "userinfo": {"username2": "xiaosan"}
    }
    # 假设获取第一层count
    gk = GetKeywords()
    res = gk.get_keywords(data, "results", "username")
    print(res)
