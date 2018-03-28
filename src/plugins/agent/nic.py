#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import traceback
import re
from src.plugins.base import BasePlugin
from lib.response import BaseResponse


class NicPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            interfaces_info = self.linux_interfaces()
            response.data = interfaces_info
        except Exception as e:
            msg = "%s dell nic plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

    def linux_interfaces(self):
        ifaces = dict()
        cmd1 = self.exec_shell_cmd('/sbin/ip link show')
        cmd2 = self.exec_shell_cmd('/sbin/ip addr show')
        ifaces = self._interfaces_ip(cmd1 + '\n' + cmd2)
        return ifaces

    def _interfaces_ip(self, out):
        ret = dict()
        right_keys = ['name', 'macaddress', 'ipaddress']
        groups = re.compile('\r?\n\\d').split(out)
        for group in groups:
            iface = None
            data = dict()
            for line in group.splitlines():
                if ' ' not in line:
                    continue
                match = re.match(r'^\d*:\s+([\w.\-]+)(?:@)?([\w.\-]+)?:\s+<(.+)>', line)
                if match:   # 匹配每个第一行
                    iface = match.groups()[0]   # eth0
                    continue
                cols = line.split()
                if len(cols) >= 2:
                    type_, value = tuple(cols[0:2])
                    iflabel = cols[-1:][0]
                    if type_ == 'inet':
                        ipaddress = value.split('/')[0]
                        data['ipaddress'] = ipaddress
                    elif type_.startswith('link'):
                        data['macaddress'] = value
            if iface:
                if iface.startswith('pan') or iface.startswith('lo') or iface.startswith('v'):
                    del iface, data
                else:
                    ret[iface] = data
                    del iface, data
        return ret
