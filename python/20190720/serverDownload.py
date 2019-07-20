#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-14 10:10
# @Author  : opsonly
# @Site    : 
# @File    : serverDownload.py
# @Software: PyCharm
import paramiko
import time


id_rsa = paramiko.RSAKey.from_private_key_file('/Users/opsonly/.ssh/id_rsa')
endtime = time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())


ip_list = {
    'aliA' : 'xxxxxxx',
    'aliB' : 'xxxxxxxxxx',
    'aliC' : 'xxxxxxxxx',
    #服务器列表
}


# 获取lavavel项目日志
def lavael_log():

    la_remote_dir = sftp.listdir('/var/www/html/')
    for i in la_remote_dir:
        print(i,end=' ')
    print('\n')
    la_obj = input('选择项目：')
    date = input('请输入日期')

    remote_file = '/var/www/html/' + la_obj + '/storage/logs/laravel-2018-' + date + '.log'
    return remote_file

# 获取nginx访问日志
def nginx_log():
    ng_remote_dir = sftp.listdir('/data/log/')
    for i in ng_remote_dir:
        print(i,end=' ')
    ng_obj = input('选择项目：')
    ng_remote_file = '/data/log/' + ng_obj + '/access.log'
    return ng_remote_file

#选择需要连接的服务器




#遍历服务器列表
def server_list():
    for k in ip_list:
        print(k,end=' ')

    print('\n')

inType = input('laravel或nginx：')
php_localFile = 'laravel' + endtime
ng_localFile = 'nginx' + endtime


server_list()

server = input('请选择要连接的server：')
scp = paramiko.Transport((ip_list[server], 23548))
scp.connect(username='ucar', pkey=id_rsa)


sftp = paramiko.SFTPClient.from_transport(scp)


if inType == 'laravel':
    try:
        remote_file = lavael_log()

        sftp.get(remote_file, php_localFile)

        print('下载成功...')
    except:
        print('下载失败，文件不存在')

else:
    try:
        remote_file = nginx_log()
        sftp.get(remote_file, ng_localFile)
        print('下载成功...')
    except:
        print('下载失败，文件不存在')

scp.close()
print('连接断开....')




