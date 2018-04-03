#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import traceback
from src.plugins.base import BasePlugin
from lib.response import BaseResponse


class CpuPlugin(BasePlugin):
    def run(self):
        response = BaseResponse()
        try:
            shell_command = 'cat /proc/cpuinfo'
            output = self.exec_shell_cmd(shell_command)
            response.data = self.parse(output)
        except Exception as e:
            msg = "%s dell cpu plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

    @staticmethod
    def parse(content):
        """
        解析shell命令返回结果
        :param content: shell 命令结果
        :return: 解析后的结果
        """
        response = {'cpu_model': '', 'cpu_physical_count': 0, 'cpu_count': 0}
        cpu_physical_set = set()
        content = content.strip()
        for item in content.split('\n\n'):
            for row_line in item.split('\n'):
                key, value = row_line.split(':')
                key = key.strip()
                if key == 'processor':
                    response['cpu_count'] += 1
                elif key == 'physical id':
                    cpu_physical_set.add(value)
                elif key == 'model name':
                    if not response['cpu_model']:
                        response['cpu_model'] = value.strip()
        response['cpu_physical_count'] = len(cpu_physical_set)
        return response
