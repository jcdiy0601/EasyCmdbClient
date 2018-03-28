#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import traceback
from src.plugins.base import BasePlugin
from lib.response import BaseResponse
from config import settings


class MemoryPlugin(BasePlugin):
    def run(self):
        response = BaseResponse()
        try:
            ret = {}
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.50.1.8.1' % (settings.community_name, self.manager_ip))
            for line in temp.split('\n'):
                line = line.strip('"')
                snmp_num = line.split()[0].split('.')[-1]
                slot = line.split()[-1].split('.')[-1]
                ret[slot] = {'slot': slot, 'sn': None, 'manufacturer': None, 'model': None, 'speed': None, 'capacity': 0}
                tmp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.50.1.23.1.%s' % (settings.community_name, self.manager_ip, snmp_num))
                sn = tmp.split('"')[-2]
                ret[slot]['sn'] = sn
                tmp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.50.1.21.1.%s' % (settings.community_name, self.manager_ip, snmp_num))
                manufacturer = tmp.split('"')[-2]
                ret[slot]['manufacturer'] = manufacturer
                tmp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.50.1.22.1.%s' % (settings.community_name, self.manager_ip, snmp_num))
                model = tmp.split('"')[-2]
                ret[slot]['model'] = model
                tmp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.50.1.15.1.%s' % (settings.community_name, self.manager_ip, snmp_num))
                speed = tmp.split()[-1]
                ret[slot]['speed'] = speed
                tmp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.50.1.14.1.%s' % (settings.community_name, self.manager_ip, snmp_num))
                capacity = int(int(tmp.split(':')[-1])/1024)
                ret[slot]['capacity'] = capacity
            response.data = ret
        except Exception as e:
            msg = "%s dell memory plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response
