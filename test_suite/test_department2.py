import unittest
from utils.send_method import SendMethod
from utils.utils import dumpJ
from utils.get_keywords import GetKeywords

"""
    对每个进口进行功能测试
    使用到的库 unittest
"""


class DepartmentTest(unittest.TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:8000/api/departments/"
        self.send = SendMethod() #发送请求
        self.gk = GetKeywords() #获取关键字值

    def test_case_01(self):
        """
        完成查询所有学院接口的测试
        """
        res = self.send.send_main("get", url=self.url)
        # count = res["count"]
        count = self.gk.get_keyword(res,'count')
        self.assertNotEqual(count, 0, "查询所有学院失败")

    def test_case_02(self):
        """
        查询单独指定的一个学院
        """
        # 定义参数
        data = {
            "$dep_id_list": "T001"
        }
        # 发送请求
        res = self.send.send_main("get", url=self.url, data=data)
        # dumpJ(res)
        # 通过count进行断言
        count = res['count']
        self.assertEqual(count, 1, "查询单个学院接口失败")

        # 通过dep_id进行断言
        # dep_id = res['results'][0]['dep_id']
        dep_id = self.gk.get_keyword(res,"dep_id")
        self.assertEqual(dep_id, "T001", "查询单个学院失败")

    def test_case_03(self):
        """
        更新院长的名字查询单个
        """
        # 参数
        data = {
            "$master_name_list": "老张"
        }
        # 发送请求
        res = self.send.send_main("get", url=self.url, data=data)

        # 通过count 断言
        count = res['count']
        self.assertEqual(count, 1, "根据院长名字查询失败")

        # 根据院长名字断言
        # master_name = res['results'][0]['master_name']
        master_name = self.gk.get_keyword(res,"master_name")
        self.assertEqual(master_name, "老张", "根据院长名字查询失败")

    def test_case_04(self):
        """
        测试学院新增接口
        """
        # 参数
        data = {
            "data": [
                {
                    "dep_id": "T01",
                    "dep_name": "测试大学院",
                    "master_name": "段教授",
                    "slogan": "学以致用"
                }
            ]
        }
        # 发送请求
        res = self.send.send_main("post", url=self.url, json=data)
        # dumpJ(res)
        # 通过create_success中的count断言
        count = res['create_success']['count']
        self.assertEqual(count, 1, "添加学院失败")

        # 通过create_success中的dep_id断言
        # dep_id = res['create_success']['results'][0]['dep_id']
        dep_id = self.gk.get_keyword(res['create_success'],"dep_id")
        self.assertEqual(dep_id, "T01", "添加学院失败")

    def test_case_05(self):
        """
        测试学院更新接口
        """
        # 准备url
        dep_id = "T01"
        url = self.url + "{}/".format(dep_id)

        # 请求数据
        dep_name = "测试大学院好"
        data = {
            "data": [
                {
                    "dep_id": dep_id,
                    "dep_name": dep_name,
                    "master_name": "段教授",
                    "slogan": "学以致用"
                }
            ]
        }

        # 发送请求
        res = self.send.send_main("put", url=url, json=data)
        # dumpJ(res)

        # 通过dep_id断言
        self.assertEqual(res['dep_id'], dep_id, "更新失败")
        # 通过dep_name断言
        self.assertEqual(res['dep_name'], dep_name, "更新失败")

    def test_case_06(self):
        """
        删除接口测试
        """
        # 参数
        data = {
            "$dep_id_list": "T01"
        }
        # 发送请求
        res = self.send.send_main("delete", url=self.url, data=data)
        # 通过状态码 204 断言
        self.assertEqual(res, 204, "删除失败")


if __name__ == '__main__':
    unittest.main()
