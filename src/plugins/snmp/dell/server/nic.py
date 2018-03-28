#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import traceback
from src.plugins.base import BasePlugin
from lib.response import BaseResponse
from config import settings


class NicPlugin(BasePlugin):
    def run(self):
        response = BaseResponse()
        try:
            ret = {}
            temp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.90.1.2.1' % (settings.community_name, self.manager_ip))
            for line in temp.split('\n'):
                line = line.strip('"')
                snmp_num = line.split()[0].split('.')[-1]
                solt = line.split()[-1].split(':')[-1]
                ret[solt] = {'macaddress': None}
                tmp = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.4.1100.90.1.15.1.%s' % (settings.community_name, self.manager_ip, snmp_num))
                macaddress = tmp.split(':')[-1].strip()
                ret[solt]['macaddress'] = macaddress
            response.data = ret
        except Exception as e:
            msg = "%s dell nic plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response
