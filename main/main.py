#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/27 15:09
# @Author  : jaeger
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @describe: 还未解决的问题: 代码结构优化, 接口加密, 双向认证证书携带,异常处理

import unittest
import ddt
import json
import yaml
import time
import HTMLTestRunner
# from BeautifulReport import BeautifulReport
from common.InspectData import InspectGlobalDict
from common.ReadCaseData import ReadXls
from common.RequestsRewrite import RequestsRW


@ddt.ddt
class RunCaseTest(unittest.TestCase):
    f = open(r"../config/env.yml", encoding="utf-8")
    config_dict = yaml.load(f, Loader=yaml.FullLoader)
    host_ = config_dict["domain"]
    data_path = config_dict["dataFiles"]
    _data_list = ReadXls(data_path, "test_case").get_xlsx()

    @classmethod
    def setUpClass(cls) -> None:
        cls.res = RequestsRW()
        cls._sess = cls.res.get_session()
        cls._sess.headers["token"] = ""
        cls.global_dict_ = {}
        cls.inspect_data = InspectGlobalDict(cls.global_dict_)

    @ddt.data(*_data_list)
    def test_001(self, test_data):
        number_, test_data_name_, method_, path_, requests_data, expect_code, global_values = \
            test_data["序号"], test_data["用例名称"], test_data["请求方法"], test_data["请求地址"], \
            json.loads(test_data["请求参数"]), test_data["状态码校验"], test_data["关键词"]
        self._sess = self.judge_token(self._sess, self.global_dict_)
        res_ = self.res.get_requests(method=method_,
                                     url=self.host_ + path_,
                                     data=self.inspect_data.resolve_data(requests_data))
        self.inspect_data.resolve_global(global_values, res_.json())
        self.assertEqual(res_.json()["code"], expect_code, msg="校验码验证未通过")

    @staticmethod
    def judge_token(sess_, global_dict):
        """
        判断请求头是否需要添加token
        :param sess_:
        :param global_dict:
        :return:
        """
        if sess_.headers["token"] == "" and "token" in global_dict:
            sess_.headers["token"] = global_dict["token"]
        return sess_


if __name__ == '__main__':
    # now = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    now = int(time.time())
    suite = unittest.TestLoader().loadTestsFromTestCase(RunCaseTest)
    report_title = '阿坝数据统计平台接口报告'
    desc = '使用了部分接口进行验证'
    with open('../ReportHTML/测试报告报告_{0}.html'.format(now), 'wb+') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f,
                                               title=report_title,
                                               description=desc
                                               )
        runner.run(suite)
