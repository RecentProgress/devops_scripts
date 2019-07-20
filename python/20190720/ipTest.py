#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-18 15:31
# @Author  : opsonly
# @Site    : 
# @File    : ipTest.py
# @Software: PyCharm


import IPy

ip = IPy.IP('172.16.0.0/26')

print(ip.len())
for i in ip:
    print(i)