#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-13 22:35
# @Author  : opsonly
# @Site    : 
# @File    : serverCommand.py
# @Software: PyCharm

import paramiko
import time

id_rsa = paramiko.RSAKey.from_private_key_file('/Users/opsonly/.ssh/id_rsa')


ip_list = {
    'aliA' : 'xxxxxx',
    'aliB' : 'xxxxxxxxx',
    'aliC' : 'xxxxxxxx',
    #服务器列表
}




def sshLog(sub,date):

    shObject = sub
    phpDir = '/var/www/html/' + shObject + '/storage/logs/laravel-' + date + '.log'
    return phpDir


for k in ip_list:
    print(k)
server = input('请选择连接的服务器：')

print('连接成功...')


ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname=ip_list[server],port=22,username='ucar',pkey=id_rsa)

sub = 'EnjoyCarCapital'

date = time.strftime("%Y-%m-%d", time.gmtime())
command = input('请输入命令: ')
cmd = command + ' ' +sshLog(sub,date)
print(cmd)

stdin, stdout, stderr = ssh.exec_command(cmd)

result = stdout.read()
print(result)
ssh.close()
