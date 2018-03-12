#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import traceback
from src.plugins.base import BasePlugin
from lib.response import BaseResponse


class DiskPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            shell_command = 'df -Pkl|grep -v Filesystem|grep -v "文件系统"'
            output = self.exec_shell_cmd(shell_command)
            response.data = self.parse(output)
        except Exception as e:
            msg = "%s linux disk plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

    @staticmethod
    def parse(content):
        response = {'total_capacity': 0}
        content = content.strip()
        total_count = 0
        for item in content.split('\n\n'):
            for row_line in item.split('\n'):
                total_count += int(row_line.split()[1])
        total_count = round(total_count/1024/1024, 2)
        response['total_capacity'] = total_count
        return response
