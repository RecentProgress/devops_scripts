#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : check-system-message.py
# @Author: Anthony.waa
# @Date  : 2019/2/12 0012
# @Desc  : PyCharm

import psutil

def memissue():
    print('内存信息：')
    mem = psutil.virtual_memory()
    # 单位换算为MB
    memtotal = mem.total/1024/1024
    memused = mem.used/1024/1024
    membaifen = str(mem.used/mem.total*100) + '%'

    print('已使用内存大小: %.2fMB' % memused)
    print('总内存大小: %.2fMB' % memtotal)
    print('内存百分比: %s'%membaifen)

def cuplist():
    print('磁盘信息：')
    disk = psutil.disk_partitions()
    diskuse = psutil.disk_usage('/')
    #单位换算为GB
    diskused = diskuse.used / 1024 / 1024 / 1024
    disktotal = diskuse.total / 1024 / 1024 / 1024
    diskbaifen = diskused / disktotal * 100
    print('已使用磁盘大小: %.2fGB' % diskused)
    print('总磁盘大小: %.2fGB' % disktotal)
    print('磁盘百分比: %.2f' % diskbaifen)

memissue()
print('*******************')
cuplist()