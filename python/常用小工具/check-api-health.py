#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : check-api-health.py
# @Author: Anthony.waa
# @Date  : 2019/3/17 0017
# @Desc  : PyCharm
import os
import requests
import json
import time

localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def apiHealth():
    # url = 'https://api.*****.cn/index.html'
    urls = {
        'api1': 'http://127.0.0.1:81/index.html',
        'api2': 'http://127.0.0.1:82/index.html',
        'api5': 'http://127.0.0.1:85/index.html',
        'api6': 'http://127.0.0.1:86/index.html',
        'api7': 'http://127.0.0.1:87/index.html',
        'api8': 'http://127.0.0.1:88/index.html',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    for name, url in urls.items():
        try:
            time.sleep(1)
            response = requests.get(url=url, headers=headers)
            if response.status_code != 200:
                postMsg('警报,警报,%s服务运行错误,请及时查看' % (name))
                apiScriptPath(name.strip())
            else:
                print('%s服务运行正常' % (name))
        except Exception as e:
            print(e)


def apiScriptPath(name):
    scriptPath = r'/root/shell'
    os.chdir(scriptPath)
    for line in os.listdir('./'):
        if line.startswith(name) and 'start' in line.strip():
            os.system('/usr/bin/sh %s' % (scriptPath + os.sep + line))
            # postMsg('/usr/bin/sh %s'%(scriptPath+os.sep+line))


# 通知钉钉
def postMsg(content):
    # 生产钉钉
    url = 'https://oapi.dingtalk.com/robot/send?access_token=***********'
    # 测试钉钉
    # url = 'https://oapi.dingtalk.com/robot/send?access_token=*********'
    HEADERS = {"Content-Type": "application/json;charset=utf-8"}
    String_textMsg = {"msgtype": "text", "text": {"content": content}}
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)


if __name__ == '__main__':
    apiHealth()
