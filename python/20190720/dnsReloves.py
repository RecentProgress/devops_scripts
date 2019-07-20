#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-20 10:21
# @Author  : opsonly
# @Site    : 
# @File    : dnsReloves.py
# @Software: PyCharm

import dns.resolver
from collections import defaultdict
hosts = ['baidu.com','weibo.com']
s = defaultdict(list)
def query(hosts):
    for host in hosts:
        ip = dns.resolver.query(host,"A")
        for i in ip:
            s[host].append(i)

    return s

for i in query(hosts):

    print(i,s[i])