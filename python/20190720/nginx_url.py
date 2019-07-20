#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-21 19:05
# @Author  : opsonly
# @Site    : 
# @File    : nginx_url.py
# @Software: PyCharm
import matplotlib.pyplot as plt

nginx_file = 'nginx2018-12-18_07:45:26'


url = {}
with open(nginx_file) as f:
    for i in f.readlines():
        s = i.split()[6]

        if s in url.keys():
            url[s] += 1
        else:
            url[s] = 1

ip = sorted(url.items(), key=lambda e:e[1], reverse=True)

ip = ip[0:10:1]

tu = dict(ip)

x = []
y = []


for k in tu:
    x.append(k)
    y.append(tu[k])
plt.title('url access')
plt.xlabel('url address')
plt.ylabel('url num')


#x轴项的翻转角度
plt.xticks(rotation=70)

#显示每个柱状图的值
for a,b in zip(x,y):
    plt.text(a, b, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)


plt.bar(x,y)
plt.legend(handles=[])

plt.show()