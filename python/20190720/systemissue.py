#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-17 17:16
# @Author  : opsonly
# @Site    : 
# @File    : systemissue.py
# @Software: PyCharm

import psutil

def memissue():
    print('内存信息：')
    mem = psutil.virtual_memory()
    memtotal = mem.total/1024/1024
    memused = mem.used/1024/1024
    membaifen = str(mem.used/mem.total*100) + '%'

    print('%.2fMB' % memused)
    print('%.2fMB' % memtotal)
    print(membaifen)

def cuplist():
    print('磁盘信息：')
    disk = psutil.disk_partitions()
    diskuse = psutil.disk_usage('/')

    diskused = diskuse.used / 1024 / 1024 / 1024
    disktotal = diskuse.total / 1024 / 1024 / 1024
    diskbaifen = diskused / disktotal * 100
    print('%.2fGB' % diskused)
    print('%.2fGB' % disktotal)
    print('%.2f' % diskbaifen)


memissue()
print('*******************')
cuplist()