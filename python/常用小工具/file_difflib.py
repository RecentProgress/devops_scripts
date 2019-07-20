#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : file_difflib.py
# @Author: Anthony.waa
# @Date  : 2018/12/15 0015
# @Desc  : PyCharm


import difflib

hd = difflib.HtmlDiff()
loads = ''
with open(r'C:\Users\Administrator\Desktop\working\practice\system-service-dev.properties', 'r',encoding='utf-8') as load:
    loads = load.readlines()
    load.close()

mems = ''
with open(r'C:\Users\Administrator\Desktop\working\practice\user-api-dev.properties', 'r',encoding='utf-8') as mem:
    mems = mem.readlines()
    mem.close()

with open('htmlout.html', 'a+') as fo:
    fo.write(hd.make_file(loads, mems))
    fo.close()

