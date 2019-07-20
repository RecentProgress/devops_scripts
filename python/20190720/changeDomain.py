#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-07-03 17:45
# @Author : opsonly
# @Site :
# @File : changeDomain.py
# @Software: PyCharm

import requests,json,os,sys,subprocess,re
domain = {
    'enjoycar.net':[
        'enjoycar','enjoyapi','agent','enjoycaragent'
    ],
    'enjoyapi.cn':[
        'v1','composer','kibana'
    ]
}

def dingdalk(text,project,ref):

    ngurl = 'https://' + text
    conten = '项目：'+ project + '\n'+'分支：' + ref + '\n' + '对应分支url链接：' + ngurl
    msg = {
        'msgtype':'text',
        'text': {
            'content': conten
        }
    }

    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    #钉钉机器人url
    url = 'https://oapi.dingtalk.com/robot/send?access_token=901ebca30bd5de8ec9257a40c26f79fe2db7bb71e4e3a83cf2e8af19eaecbde7'

    #推送消息
    res = requests.post(url=url,headers=headers,data=json.dumps(msg))
    return res

def updateIt():
    os.chdir(prodir)
    gpl = 'git pull origin ' + ref
    pd = 'pwd'
    cmd1 = gpl + '&&' +pd

    ret = subprocess.getstatusoutput(cmd1)

    res.append(ret)

    s = subprocess.getstatusoutput('pwd')

    res.append(s)

    if ref.startswith('feature'):
        cpenv = 'cp .env.feature .env'
    else:
        cpenv = 'cp .env.develop .env'

    compose = 'composer install'

    cmd2 = cpenv + '&&' + compose
    ret2 = subprocess.getstatusoutput(cmd2)
    res.append(ret2)

    ret3 = subprocess.getstatusoutput('/usr/local/php7/bin/php artisan queue:restart')

    res.append(ret3)

    return res


project = sys.argv[1]
ref = sys.argv[2]
giturl = sys.argv[3]


if project in domain['enjoycar.net']:
    doname = 'enjoycar.net'
else:
    doname = 'enjoyapi.cn'


oridir = project + '-' + ref

dirname = re.sub(r'[/_]','-',oridir) + '.' + doname

webdir = '/webdata/var/www/test/'
prodir = webdir + dirname

oriconf = '/WebUpdate/51ucar-dev-agent.conf'
ngconf = '/etc/nginx/conf.d/' + dirname + '.conf'

res = []

if os.path.isdir(prodir):
    updateIt()
else:
    cdir = 'cd ' + webdir
    gcl = 'git clone -b ' + ref + ' ' + giturl + ' ' + dirname
    cdpro = 'cd ' + dirname
    cmd1 = cdir + '&&' + gcl + '&&' + cdpro

    res1 = subprocess.getstatusoutput(cmd1)

    res.append(res1)
    updateIt()

    cpconf = 'cp ' + oriconf + ' ' + ngconf
    sed1 = 'sed -i -r ' + '\"s@root (/[A-Za-z]+)+;@root ' + prodir + '/public;@g\"' + ' ' + ngconf
    sed2 = 'sed -i -r \"s@server_name _@server_name ' + dirname + '@g\"' + ' ' + ngconf
    sed3 = 'sed -i -r \"s@https://x.51ucar.cn@https://' + dirname + '@g\"' + ' ' + ngconf
    cmd3 = cpconf + '&&' + sed1 + '&&' + sed2 + '&&' + sed3

    res3 = subprocess.getstatusoutput(cmd3)

    res.append(res3)

    sdng = 'sudo -u ucar nginx -s reload'
    print(res)

    dingdalk(dirname,project,ref)

