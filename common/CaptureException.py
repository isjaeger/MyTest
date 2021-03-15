#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 11:33
# @Author  : jaeger
# @mail    : isjaeger@qq.com
# @File    : CaptureException.py
# @Software: PyCharm
# @describe: 触发异常捕获
import sys


class CaptureEx:

    def __init__(self, value, exception_msg):
        """
        当前置参数未获取成功自动终止程序,避免浪费时间, 例如token未获取成功等;
        :param value: 判断的值
        :param exception_msg: 返回的程序终止原因
        """
        self._value = value
        self._exception_msg = exception_msg

    def respect_exception(self):
        exception_list = ['', None]
        try:
            if self._value in exception_list:
                raise
        except Exception:
            print(self._exception_msg)
            sys.exit()
