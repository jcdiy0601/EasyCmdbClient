#!/usr/bin/env python
# Author: 'JiaChen'

import traceback
from src.plugins.base import BasePlugin
from lib.response import BaseResponse
from config import settings
import re


class BasicPlugin(BasePlugin):
    """获取h3c交换机信息"""
    def run(self):
        response = BaseResponse()
        try:
            response.data = {'sn': None, 'port_number': 0, 'run_time': 0, 'device_name': None, 'model': None, 'basic_info': None}
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.2.1.47.1.1.1.1.11' % (settings.community_name, self.manager_ip))
            temp_list = temp.split('\n')
            for item in temp_list:
                if item.split('"')[1]:
                    sn = item.split('"')[1].strip()
                    response.data['sn'] = sn
            port_number = response.data['port_number']
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.2.1.2.2.1.2' % (settings.community_name, self.manager_ip))
            temp_list = temp.split('\n')
            for item in temp_list:
                if re.match('GigabitEthernet', item.split(':')[-1].strip()):
                    port_number += 1
            response.data['port_number'] = port_number
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.2.1.1.3.0' % (settings.community_name, self.manager_ip))
            run_time = int(temp.split(')')[-1].strip().split()[0])
            response.data['run_time'] = run_time
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.2.1.1.5.0' % (settings.community_name, self.manager_ip))
            device_name = temp.split(':')[-1].strip()
            response.data['device_name'] = device_name
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.2.1.47.1.1.1.1.2.2' % (settings.community_name, self.manager_ip))
            model = temp.split('"')[1].split()[1].strip()
            response.data['model'] = model
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.2.1.1.1.0' % (settings.community_name, self.manager_ip))
            basic_info = temp.split(':')[-1].strip()
            response.data['basic_info'] = basic_info
        except Exception as e:
            msg = "%s h3c switch plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response
