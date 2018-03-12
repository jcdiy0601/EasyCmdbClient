#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import sys
import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

from src.scripts import client

if __name__ == '__main__':
    client()
