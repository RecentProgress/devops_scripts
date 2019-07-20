#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @Time    : 2019-05-31 16:00
# @Author  : Anthony.long
# @Site    :
# @File    : check_https_dated.py
# @Software: PyCharm


# 查询域名证书到期情况

import re
import time
import subprocess
from datetime import datetime
from io import StringIO


def main(domain):
    f = StringIO()
    start_time = time.strftime("%Y-%m-%d %X", time.localtime())

    comm = ""
    result = subprocess.getstatusoutput(comm)
    f.write(result[1])

    end_time = time.strftime("%Y-%m-%d %X", time.localtime())

    start_date = re.search('(start date:.*?\n)', f.getvalue(), re.S).group().strip().split(': ')[1]
    expire_date = re.search('(expire date:.*?\n)', f.getvalue(), re.S).group().strip().split(': ')[1]
    subjectAltName_name = re.search('(subjectAltName:.*?\n)', f.getvalue(), re.S).group().strip().split(': ')[1]
    issuer = re.search('(issuer:.*?\n)', f.getvalue(), re.S).group().strip().split(': ')[1]

    # # time 字符串转时间数组
    start_date = time.strptime(start_date, "%b %d %H:%M:%S %Y GMT")
    start_date_st = time.strftime("%Y-%m-%d %H:%M:%S", start_date)
    # # datetime 字符串转时间数组
    expire_date = datetime.strptime(expire_date, "%b %d %H:%M:%S %Y GMT")
    expire_date_st = datetime.strftime(expire_date, "%Y-%m-%d %H:%M:%S")

    # # 剩余天数
    remaining = (expire_date - datetime.now()).days

    if int(remaining) >= 4:
        # print(domain)
        print('域名:', domain)
        print('通用名:', subjectAltName_name)
        print('证书开始使用时间:', start_date_st)
        print('证书到期时间:', expire_date_st)
        print('证书剩余可用时间: {remaining}天')
        print('颁发机构:', issuer)
        print('*' * 30)
        time.sleep(0.5)


if __name__ == "__main__":
    # with open('domains.txt','r',encoding="utf-8") as file:
    # with open('onlineDomains.txt', 'r', encoding="utf-8") as file:
    with open('/Users/ianthony/Desktop/project/devops/日常小工具/online.txt', 'r', encoding="utf-8") as file:
    # with open('tmp.txt', 'r', encoding="utf-8") as file:
        for domain in file:
            main(domain.strip())
