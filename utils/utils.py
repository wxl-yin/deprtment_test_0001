import json
"""封装工具"""



def dumpJ(dict_data):
    """
    将字典格式化输出
    :param dict_data: 字典对象
    :return:
    """
    json_str = json.dumps(dict_data, indent=2, ensure_ascii=False)
    print(json_str)