#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen


class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.message = None
        self.error = None
