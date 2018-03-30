#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from src.plugins.basic import BasicPlugin
from config import settings
import importlib


def get_server_info(manager_ip=None, info_dict=None):
    """
    获取服务器基本信息
    :param manager_ip: 管理IP，Snmp模式要用到管理IP
    :return:
    """
    # 获取基本信息
    response = BasicPlugin(manager_ip, info_dict).execute()
    # 如果基本信息获取报错返回response
    if not response.status:
        return response
    # 如果采集类型为Agent
    if settings.MODE == 'agent':
        # 执行收集资产的各类插件
        for k, v in settings.AGENT_PLUGINS_DICT.items():
            module_path, cls_name = v.rsplit('.', 1)    # ['src.plugins.agent.disk', 'DiskPlugin']
            cls = getattr(importlib.import_module(module_path), cls_name)
            res = cls(manager_ip).execute()
            response.data[k] = res
    # 如果采集类型为Snmp
    elif settings.MODE == 'snmp':
        # 执行收集资产的各类插件
        if info_dict['manufacturer'] == 'dell':
            plugin_dict = settings.SNMP_DELL_PLUGINS_DICT[info_dict['device_type']]
            for k, v in plugin_dict.items():
                module_path, cls_name = v.rsplit('.', 1)
                cls = getattr(importlib.import_module(module_path), cls_name)
                res = cls(manager_ip, info_dict).execute()
                response.data[k] = res
        elif info_dict['manufacturer'] == 'h3c':
            plugin_dict = settings.SNMP_H3C_PLUGINS_DICT[info_dict['device_type']]
            for k, v in plugin_dict.items():
                module_path, cls_name = v.rsplit('.', 1)
                cls = getattr(importlib.import_module(module_path), cls_name)
                res = cls(manager_ip, info_dict).execute()
                response.data[k] = res
        elif info_dict['manufacturer'] == 'juniper':
            plugin_dict = settings.SNMP_JUNIPER_PLUGINS_DICT[info_dict['device_type']]
            for k, v in plugin_dict.items():
                module_path, cls_name = v.rsplit('.', 1)
                cls = getattr(importlib.import_module(module_path), cls_name)
                res = cls(manager_ip, info_dict).execute()
                response.data[k] = res
    return response
