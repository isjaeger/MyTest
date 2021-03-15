#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 13:49
# @Author  : jaeger
# @mail    : isjaeger@qq.com
# @File    : RequestsRewrite.py
# @Software: PyCharm
# @describe: 封装requests模块

import requests


class RequestsRW:

    def __init__(self):
        self._sess = requests.Session()

    def get_session(self) -> object:
        return self._sess

    def get_requests(self, method, url,
                     data=None, json=None) -> object:
        res = self._sess.request(method=method, url=url, data=data, json=json)
        return res
