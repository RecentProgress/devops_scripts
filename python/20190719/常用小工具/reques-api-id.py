#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @Time    : 2019-04-18 10:44
# @Author  : Anthony.long
# @Site    : 
# @File    : tornado-demo.py
# @Software: PyCharm


import requests
import time


def requestId(id):
    # 测试环境
    url = 'https://***.***.cn/actionService/gateway?sn=BatchQuartz&mn=createNewBookPackClass&packageId='

    # 生产环境
    # url = 'https://***.***.cn/actionService/gateway?sn=BatchQuartz&mn=createNewBookPackClass&packageId='

    response = requests.get('%s%s' % (url, id))
    localTimes = time.strftime('%Y.%m.%d %H:%m:%s', time.localtime(time.time()))

    if response.status_code == 200:
        print(response.text)
    else:
        with open('./requestId.log', 'a+', encoding="utf-8") as file:
            file.writelines('%s,%s%s,%s\n' % (localTimes, url, id, response.text))


if __name__ == '__main__':

    # 生产环境
    # idList = [3250, 3251, 3252, 3253, 3254, 3255, 3288, 3289, 3290, 3291, 3292, 3293, 3294, 3295, 3296, 3297, 3298,3299, 3344, 3345, 3346, 3347, 3348, 3349, 3455, 3456, 3457, 3458, 3495, 3496, 3497, 3498, 3499, 3500]

    # 测试环境
    idList = [4113, 4256, 4130]

    for i in idList:
        requestId(i)
