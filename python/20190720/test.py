#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-20 15:19
# @Author  : opsonly
# @Site    : 
# @File    : redisdel.py
# @Software: PyCharm

import redis

password = 'Kasd&(asd)213aH'

objRedis = {
    '正式环境': 5343,
    '预正式环境': 5342,
}
port = input("正式环境\n预正式环境\n")
db = input('输入数据库:')

try:
    r = redis.Redis(host='172.18.109.227',port=objRedis[port],db=db,password=password)

    #输入要匹配的键名
    id = input('请输入要执匹配的字段：')
    arg = '*' + id + '*'

    n = r.keys(arg)
    #查看匹配到键值
    for i in n:
        print(i.decode('utf-8'))

    #确定清除的键名
    delid = input('输入要删除的键：')

    r.delete(delid)

    print('清除缓存 %s 成功' % delid)
except:
    print("异常中断")


