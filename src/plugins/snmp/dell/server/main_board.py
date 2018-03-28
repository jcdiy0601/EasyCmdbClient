#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import traceback
from src.plugins.base import BasePlugin
from lib.response import BaseResponse
from config import settings


class MainBoardPlugin(BasePlugin):
    def run(self):
        response = BaseResponse()
        try:
            response.data = {'sn': None, 'fast_server_number': None, 'model': None}
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.2.1.1.11.0' % (settings.community_name, self.manager_ip))
            sn = temp.split('"')[-2]
            response.data['sn'] = sn
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.1.3.3.0' % (settings.community_name, self.manager_ip))
            fast_server_number = temp.split('"')[-2]
            response.data['fast_server_number'] = fast_server_number
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.1.3.12.0' % (settings.community_name, self.manager_ip))
            model = temp.split('"')[-2]
            response.data['model'] = model
        except Exception as e:
            msg = "%s dell mainboard plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response
