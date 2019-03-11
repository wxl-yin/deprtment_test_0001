"""
    自动化接口测试框架入口, 只需要访问该文件即可
    修改
    完成的事情:
        1. 获取所有的测试用例
        2. 执行测试用例生成测试报告
        3. 将测试报告以邮件的形式发送
"""
import os
import smtplib
import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from plugins.HTMLTestRunnerPlugins import HTMLTestRunner
import time


def find_suites(suite_path, rule):
    """
    发现所有的测试用例
    :param suite_path: 用例的路径
    :param rule:  用例文件的规则
    :return: 返回测试用例
    """
    discover = unittest.defaultTestLoader.discover(start_dir=suite_path,
                                                   pattern=rule,
                                                   top_level_dir=None
                                                   )
    return discover


def create_reports(suites, report_path):
    """
    执行用例并生成报告
    :param suites:  测试用例
    :param report_path:  测试报告目录
    :return: 返回测试报告的路径
    """
    # 获取文件句柄
    # 准备文件的路径
    filename = time.strftime("%Y%m%d_%H%M%S_%p") + "_report.html"
    # 文件路径
    file_path = os.path.join(report_path, filename)
    # 打开文件
    file_fp = open(file_path, "wb")
    runner = HTMLTestRunner(title="自动化接口测试报告",
                            description="自动化接口测试报告",
                            retry=0,
                            verbosity=2,
                            stream=file_fp
                            )
    # 执行
    runner.run(suites)
    # 关闭文件
    file_fp.close()

    # 返回测试报告路径
    return file_path


def send_mail(smtp_user, smtp_password, recieve_user, subject, report_path, smtp_port=465, smtp_server="smtp.qq.com"):
    """
    发送邮件
    :param smtp_user: smtp用户名
    :param smtp_password: smtp授权码
    :param recieve_user: 收件人地址
    :param subject: 主题
    :param report_path: 报告地址
    :param smtp_port: 端口
    :param smtp_server: 服务器地址
    :return:
    """
    filename = report_path  # 附件的路径
    # 读取文件内容
    with open(filename, 'rb') as fp:
        file_body = fp.read()

    # 创建对象 MIMEMultipart() (容器, 附件, 文本)
    mime_message = MIMEMultipart()

    # 容器中添加文本
    text = MIMEText(_text=file_body, _subtype="html", _charset="utf-8")
    # 将文本添加到容器里面
    mime_message.attach(text)

    # 编译文件内容
    file_message = MIMEText(_text=file_body, _subtype="base64", _charset="utf-8")
    # 额外设置
    file_message["Content-Type"] = "application/octet-stream"  # 二进制流
    # 内容规定 attachment 附件 filename 下载时候的文件名字
    # print(os.path.basename(filename)) #获取路径中文件的名字
    file_message["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.basename(filename))

    # 将编译好的文件放到容器中
    mime_message.attach(file_message)

    # 设置发件人和收件人和主体
    mime_message['from'] = smtp_user
    mime_message['to'] = ";".join(recieve_user)
    mime_message['subject'] = subject

    # ======================发送邮件==============================
    # 创建对象
    smtp = smtplib.SMTP_SSL()
    # 链接服务器
    smtp.connect(host=smtp_server, port=smtp_port)
    # 登录
    smtp.login(user=smtp_user, password=smtp_password)
    # 发送
    smtp.sendmail(from_addr=mime_message['from'], to_addrs=recieve_user, msg=mime_message.as_string())
    # 退出
    smtp.quit()


if __name__ == '__main__':
    # >>>>>1获取所有的测试用例
    base_dir = os.path.dirname(os.path.realpath(__file__))  # 项目根目录
    # 需要指定测试用例所在的路径(绝对路径)
    suite_path = os.path.join(base_dir, "test_suite")  # 目录连接
    # 调用发现测试用例的函数
    rule = "test_*.py"
    suites = find_suites(suite_path, rule=rule)

    # >>>>>2.执行测试用例生成测试报告
    report_path = os.path.join(base_dir, "reports")
    report_filename = create_reports(suites, report_path)
    # print(report_filename)

    # >>>>>>3.将测试报告以邮件的形式发送
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    smtp_user = "516371998@qq.com"
    smtp_password = "leesdbxkyuqfbgcb"
    subject = "自动化接口测试报告"
    recieve_user = ["eric_cdycq@163.com"]

    # 发送
    send_mail(smtp_user=smtp_user,
              smtp_password=smtp_password,
              recieve_user=recieve_user,
              subject=subject,
              report_path=report_filename
              )
    print("发送邮件成功")
