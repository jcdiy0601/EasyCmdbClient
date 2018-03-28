#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import traceback
from src.plugins.base import BasePlugin
from lib.response import BaseResponse


class MemoryPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            shell_command = 'free -m|grep Mem'
            output = self.exec_shell_cmd(shell_command)
            response.data = self.parse(output)  # Mem: 988 825 163 3 124 312
        except Exception as e:
            msg = "%s dell memory plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

    @staticmethod
    def parse(content):
        response = {
            'total_capacity': int(content.split()[1])
        }
        return response
