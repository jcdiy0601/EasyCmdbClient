#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from src.client import AutoAgent
from src.client import AutoSnmp
from config import settings


def client():
    # Agent模式
    if settings.MODE == 'agent':
        cli = AutoAgent()
    # Snmp模式
    elif settings.MODE == 'snmp':
        cli = AutoSnmp()
    # 非Agent或Snmp模式，则报异常
    else:
        raise Exception('请配置资产采集模式，如：agent、snmp')
    cli.process()
