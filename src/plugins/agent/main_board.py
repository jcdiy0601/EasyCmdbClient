#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import traceback
from src.plugins.base import BasePlugin
from lib.response import BaseResponse


class MainBoardPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            shell_command = 'dmidecode -t1'
            output = self.exec_shell_cmd(shell_command)
            response.data = self.parse(output)
        except Exception as e:
            msg = "%s linux mainboard plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

    @staticmethod
    def parse(content):
        response = {}
        key_map = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'model',
            'Serial Number': 'sn',
        }
        for item in content.split('\n'):
            row_data = item.strip().split(':')
            if len(row_data) == 2:
                if row_data[0] in key_map:
                    response[key_map[row_data[0]]] = row_data[1].strip() if row_data[1] else row_data[1]
        return response
