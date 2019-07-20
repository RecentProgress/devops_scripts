#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-18 17:41
# @Author  : opsonly
# @Site    :
# @File    : gitlabCi.py
# @Software: PyCharm


from flask import Flask,request,render_template,make_response,Response
import json,os,re,requests
import subprocess
import re

app = Flask(__name__)
null = ""
cmd = "/var/www/html/"
@app.route('/test',methods=['POST'])
def hello():
    json_dict = json.loads(request.data)

    name = json_dict['event_name']

    #字符串截取分支名
    ref = json_dict['ref'][11:]

    ssl = json_dict['project']['url']

    #gitlab项目名
    project = json_dict['project']['name']

    #gitlab分组名
    namespace = json_dict['project']['namespace']

    hostfix = re.compile(r'hostfix/*')
    feature = re.compile(r'feature/*')


    if name == 'push':
        if namespace == 'it':

            #预上线分支
            if ref == 'master':
                cmd = './itmaster.sh ' + project + ref + ' ' + namespace
                s = subprocess.getoutput(cmd)
                return Response(s)

            # 测试分支
            elif ref == 'develop':
                cmd = './itdevelop.sh ' + project + ref + ' ' + namespace
                s = subprocess.getoutput(cmd)
                return Response(s)

            #开发分支
            elif hostfix.match(ref) and feature.match(ref):
                cmd = './itOwn.sh' + project + ref + ' ' + namespace + '' + ssl
                s = subprocess.getoutput(cmd)
                return Response(s)

        elif namespace == 'web':
            if ref == 'master':
                cmd = './webMaster.sh ' + project + ref + ' ' + namespace
                s = subprocess.getoutput(cmd)
                return Response(s)
            elif ref == 'develop':
                cmd = './webDevelop.sh ' + project + ref + ' ' + namespace
                s = subprocess.getoutput(cmd)
                return Response(s)
                # 开发分支
            elif hostfix.match(ref) and feature.match(ref):
                cmd = './webOwn.sh' + project + ref + ' ' + namespace
                s = subprocess.getoutput(cmd)
                return Response(s)



    elif name =='merge_request':

        #可以定义一个钉钉推送，每次直接点开链接就能直达gitlab合并界面
        pass
    else:
        return Response('未触发事件')



if __name__ == '__main__':
    app.run()


