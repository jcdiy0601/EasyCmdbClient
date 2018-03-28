#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import os

# 项目家目录
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 采集资产模式，默认为agent
MODE = 'snmp'

# 资产信息API
ASSET_API = 'http://10.10.30.93/cmdb_api/v1/asset'
"""
POST时，返回值：{'code': xx, 'message': 'xx'}
 code:
    - 201 成功;
    - 401 接口授权失败;
    - 404 数据库中资产不存在
    - 400 资产更新异常
"""

# 用于API认证的KEY
KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'

# 用于API认证的请求头
AUTH_KEY_NAME = 'cmdb-api-auth-key'

# 错误日志
ERROR_LOG_FILE = os.path.join(BASEDIR, "log", 'error.log')

# 运行日志
RUN_LOG_FILE = os.path.join(BASEDIR, "log", 'run.log')

# Agent模式保存服务器唯一ID的文件
# CERT_FILE_PATH = os.path.join(BASEDIR, 'config', 'cert')

# Agent模式服务器唯一值hostname
HOSTNAME = 'fthw-cmdb-test-web1_192.168.222.10'

# agent采集硬件数据的插件
AGENT_PLUGINS_DICT = {
    'cpu': 'src.plugins.agent.cpu.CpuPlugin',
    'disk': 'src.plugins.agent.disk.DiskPlugin',
    # 'main_board': 'src.plugins.agent.main_board.MainBoardPlugin',
    'memory': 'src.plugins.agent.memory.MemoryPlugin',
    'nic': 'src.plugins.agent.nic.NicPlugin',
}

# snmp采集dell设备数据的插件
SNMP_DELL_PLUGINS_DICT = {
    'server': {
        'cpu': 'src.plugins.snmp.dell.server.cpu.CpuPlugin',
        'disk': 'src.plugins.snmp.dell.server.disk.DiskPlugin',
        'main_board': 'src.plugins.snmp.dell.server.main_board.MainBoardPlugin',
        'memory': 'src.plugins.snmp.dell.server.memory.MemoryPlugin',
        'nic': 'src.plugins.snmp.dell.nic.NicPlugin',
    }
}

# snmp采集h3c设备数据的插件
SNMP_H3C_PLUGINS_DICT = {
    'switch': {
        'basic': 'src.plugins.snmp.h3c.switch.basic.BasicPlugin',
    }
}

# snmp community name
community_name = 'public'
