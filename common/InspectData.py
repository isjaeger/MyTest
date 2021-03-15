#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 11:33
# @Author  : jaeger
# @mail    : isjaeger@qq.com
# @File    : InspectData.py
# @Software: PyCharm
# @describe: 判断response的字段的参数是否有需要添加到全局变量字典中, 解决上下游参数传递的问题

import json
import jsonpath
import re


class InspectGlobalDict:

    def __init__(self, global_dict):
        self._global_dict = global_dict

    def resolve_data(self, dict_data) -> dict:
        """
        判断请求字典是否需要根据全局变量字典进行更新
        :param dict_data: 请求数据, str格式
        :return: 返回更新后的的接口请求data字典
        """
        dict_str = json.dumps(dict_data, ensure_ascii=False)
        key_list = re.findall("\$\[(.*?)\]", dict_str)
        if key_list:
            for i in range(len(key_list)):
                re_model = "\$\[({0})\]".format(key_list[i])
                dict_str = re.sub(re_model, str(self._global_dict[key_list[i]]), dict_str)
        return json.loads(dict_str)

    def resolve_global(self, global_variable, response_body) -> dict:
        """
        判断接口返回值是否需要更新到变量字典
        :param global_variable: 全局变量字段,str
        :param response_body: 接口的响应值, dict
        :return: 更新后的全局变量字典
        """
        if global_variable != "":
            global_variable = global_variable.strip().split(",")
            global_variable = list(filter(None, global_variable))
            for i in range(len(global_variable)):
                self._global_dict[global_variable[i]] = \
                    jsonpath.jsonpath(response_body, "$..{0}".format(global_variable[i]))[0]
        return self._global_dict
