#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 11:29
# @Author  : jaeger
# @mail    : isjaeger@qq.com
# @File    : ReadCaseData.py
# @Software: PyCharm
# @describe: 读取xls中的测试数据

import xlrd


class ReadXls:

    def __init__(self, path, sheet_name):
        """
        :param path: xlsx的读取路径
        :param sheet_name: 需要读取的sheet页名
        """
        work_book = xlrd.open_workbook(path)
        self._mySheet = work_book.sheet_by_name(sheet_name)

    def get_xlsx(self) -> list:
        """
        :return: 元素是由dict组成的list
        """
        list_data = []
        for i in range(1, self._mySheet.nrows):
            data = self._mySheet.row_values(i)
            dict_data = {}
            for k in range(len(self._mySheet.row_values(0))):
                dict_data[self._mySheet.row_values(0)[k]] = data[k]
            list_data.append(dict_data)
        return list_data
