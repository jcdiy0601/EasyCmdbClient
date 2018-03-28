#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from lib.log import Logger
from config import settings


class BasePlugin(object):
    """
    插件基类
    """
    def __init__(self, manager_ip=None, info_dict=None):
        # 初始化日志
        self.logger = Logger()
        # 初始化采集类型列表
        self.mode_list = ['agent', 'snmp']
        # 如果settings文件中有MODE变量
        if hasattr(settings, 'MODE'):
            # 初始化采集类型
            self.mode = settings.MODE
            # 如果采集类型为snmp
            if self.mode == 'snmp':
                # 初始化管理ip
                self.manager_ip = manager_ip
                # 初始化hostname
                self.hostname = manager_ip
                # 初始化value_dict
                self.info_dict = info_dict
        # 如果settings文件中没有MODE变量
        else:
            # 初始化采集类型为Agent
            self.mode = 'agent'

    def agent(self, cmd):
        """
        Agent执行命令方法
        :param cmd: 命令
        :return:
        """
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def snmp(self, cmd):
        """
        Snmp执行命令方法
        :param cmd: 命令
        :return:
        """
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def exec_shell_cmd(self, cmd):
        """
        执行命令入口方法
        :param cmd: 命令
        :return:
        """
        if self.mode not in self.mode_list:
            raise Exception("settings.mode必须是['agent', 'snmp']中的一种")
        func = getattr(self, self.mode)
        output = func(cmd)
        return output

    def execute(self):
        return self.run()

    def run(self):
        raise Exception('必须实现run方法')