#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import traceback
from src.plugins.base import BasePlugin
from lib.response import BaseResponse
from config import settings


class CpuPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            response.data = {'cpu_model': None, 'cpu_physical_count': 0, 'cpu_count': 0}
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.30.1.23.1' % (settings.community_name, self.manager_ip))
            cpu_model = temp.split('"')[1]
            response.data['cpu_model'] = cpu_model
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.30.1.23.1|wc -l' % (settings.community_name, self.manager_ip))
            cpu_physical_count = int(temp)
            response.data['cpu_physical_count'] = cpu_physical_count
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.30.1.18.1' % (settings.community_name, self.manager_ip))
            cpu_count = 0
            for line in temp.split('\n'):
                cpu_count += int(line.split(':')[-1])
            response.data['cpu_count'] = cpu_count
        except Exception as e:
            msg = "%s linux cpu plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response
