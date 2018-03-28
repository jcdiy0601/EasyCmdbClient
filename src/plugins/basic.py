#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import traceback
from src.plugins.base import BasePlugin
from lib.response import BaseResponse
from config import settings


class BasicPlugin(BasePlugin):
    def os_version(self):
        """
        获取系统版本
        :return:
        """
        if self.mode == 'agent':
            output = self.exec_shell_cmd('cat /etc/redhat-release')
            return output.strip()
        elif self.mode == 'snmp' and self.info_dict['manufacturer'] == 'dell':
            output = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.1.3.6.0' % (settings.community_name, self.manager_ip)).split('"')[-2]
            if 'VMware' in output:
                output_list = output.split()
                output = ' '.join(output_list[0:3])
            elif 'Microsoft' in output:
                output_list = output.split()
                output = ' '.join(output_list[0:4])
            else:
                temp1 = output
                temp2 = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.1.3.14.0' % (settings.community_name, self.manager_ip)).split('"')[-2]
                output_list = temp2.split()
                output = temp1 + ' ' + ' '.join(output_list[0:3])
            return output.strip()

    def os_hostname(self):
        """
        获取主机名
        :return:
        """
        if self.mode == 'agent':
            output = settings.HOSTNAME
            return output.strip()
        elif self.mode == 'snmp' and self.info_dict['manufacturer'] == 'dell':
            output = self.exec_shell_cmd('snmpwalk -v 2c -c %s %s .1.3.6.1.4.1.674.10892.5.1.3.1.0' % (settings.community_name, self.manager_ip)).split('"')[-2]
            return output.strip()

    def run(self):
        response = BaseResponse()
        if self.mode == 'agent':  # 软件服务器
            try:
                ret = {
                    'os_version': self.os_version(),
                    'hostname': self.os_hostname(),
                    'client_type': settings.MODE
                }
                response.data = ret
            except Exception as e:
                msg = '%s BasicPlugin Error: %s'
                self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
                response.status = False
                response.error = msg % (self.hostname, traceback.format_exc())
        elif self.info_dict['device_type'] == 'server':
            try:
                ret = {
                    'os_version': self.os_version(),
                    'hostname': self.os_hostname(),
                    'client_type': settings.MODE,
                    'device_type': self.info_dict['device_type'],
                    'manufacturer': self.info_dict['manufacturer']
                }
                response.data = ret
            except Exception as e:
                msg = '%s BasicPlugin Error: %s'
                self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
                response.status = False
                response.error = msg % (self.hostname, traceback.format_exc())
        else:
            try:
                ret = {
                    'client_type': settings.MODE,
                    'device_type': self.info_dict['device_type'],
                    'manufacturer': self.info_dict['manufacturer']
                }
                response.data = ret
            except Exception as e:
                msg = '%s BasicPlugin Error: %s'
                self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
                response.status = False
                response.error = msg % (self.hostname, traceback.format_exc())
        return response
