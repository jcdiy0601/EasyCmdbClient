#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import json
import time
import hashlib
import requests
from concurrent.futures import ThreadPoolExecutor
from config import settings
from lib.log import Logger
from src import plugins
from lib.serialize import Json


class AutoBase(object):
    def __init__(self):
        # 初始化api的url
        self.asset_api = settings.ASSET_API
        # 初始化key
        self.key = settings.KEY
        # 初始化key_name
        self.key_name = settings.AUTH_KEY_NAME

    def auth_key(self):
        """
        为api接口认证提供加密加盐的串
        :return:
        """
        ha = hashlib.md5(self.key.encode('utf-8'))
        time_span = time.time()
        ha.update(bytes('%s|%f' % (self.key, time_span), encoding='utf-8'))
        encryption = ha.hexdigest()
        result = '%s|%f' % (encryption, time_span)
        return {self.key_name: result}      # {'cmdb_api_auth-key': 'xxxx|12312'}

    def get_asset(self):
        """
        get方式从api接口获取在线的硬件服务器管理IP
        :return: {'status': True, 'error': None, 'message': None, 'data': {'10.255.1.21': {'device_type': 'switch', 'manufacturer': 'h3c'}, '10.10.2.10': {'device_type': 'server', 'manufacturer': 'dell'}}}
        :return:
        """
        try:
            headers = {}
            headers.update(self.auth_key())
            response = requests.get(url=self.asset_api, headers=headers)
        except Exception as e:
            response = e
        return response.json()

    def post_asset(self, msg, callback=None):
        """
        post方式向api接口提交数据
        :param msg: 要提交的数据
        :param callback: 回调函数
        :return:
        """
        status = True
        try:
            headers = {}
            headers.update(self.auth_key())
            response = requests.post(url=self.asset_api, headers=headers, json=msg)
        except Exception as e:
            response = e
            status = False
        if callback:
            callback(status, response)

    def process(self):
        """
        派生类需要继承此方法，用于处理请求的入口
        :return:
        """
        raise NotImplementedError('必须实现process方法')

    def callback(self, status, response):
        """
        提交资产后的回调函数
        :param status: 是否请求成功
        :param response: 请求成功：则是响应内容，请求失败：则是异常对象
        :return:
        """
        if not status:
            Logger().log(str(response), False)
            return
        ret = json.loads(response.text)
        if ret['code'] == 201:
            Logger().log(ret['message'], True)
        else:
            Logger().log(ret['message'], False)


class AutoAgent(AutoBase):
    def __init__(self):
        # 初始化hostname
        self.hostname = settings.HOSTNAME
        super(AutoAgent, self).__init__()

    def process(self):
        """
        获取软件服务器资产信息
        cmdb数据库中保存的hostname要与Agent端settings文件中设置的HOSTNAME保持一致
        :return:
        """
        # 获取资产
        server_info = plugins.get_server_info()
        # 如果获取失败退出此函数
        if not server_info.status:
            return
        # 序列化获取到的资产
        server_json = Json.dumps(server_info.data)
        # 发送资产数据到api接口
        self.post_asset(server_json, self.callback)


class AutoSnmp(AutoBase):
    def process(self):
        """
        获取硬件服务器资产信息
        :return:
        """
        # 获取要通过snmp获取的硬件服务器管理IP
        # {'status': True, 'error': None, 'message': None, 'data': {'10.255.1.21': {'device_type': 'switch', 'manufacturer': 'h3c'}, '10.10.2.10': {'device_type': 'server', 'manufacturer': 'dell'}}}
        task = self.get_asset()
        # 如果获取失败，写入日志
        if not task['status']:
            Logger().log(task['message'], False)
        # 启动多线程获取数据
        pool = ThreadPoolExecutor(10)
        for key, value in task['data'].items():
            manager_ip = key
            info_dict = value
            pool.submit(self.run, manager_ip, info_dict)
        pool.shutdown(wait=True)

    def run(self, manager_ip, info_dict):
        # 获取硬件服务器资产信息
        server_info = plugins.get_server_info(manager_ip=manager_ip, info_dict=info_dict)
        # 序列化获取到的资产
        server_json = Json.dumps(server_info.data)
        # 发送资产数据到api接口
        self.post_asset(server_json, self.callback)
