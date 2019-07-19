#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : check-process-and-send-email.py
# @Author: Anthony.waa
# @Date  : 2018/11/23 0023
# @Desc  : PyCharm

import os
import smtplib
from email.mime.text import MIMEText
servicelist = ['study-center-api','study-center-service','system-api','system-service','user-api','user-service']
isexist = []        # 进程存在列表
notexist = []       # 进程不存在列表
# 判断服务进程是否存在
def testprocess():
    systemlist = []
    for line in servicelist:
        Runpid = os.popen("ps -ef|grep %s|grep -v 'grep'|awk -F ' ' '{print $13}'|awk -F '=' '{print $2}'" % line)
        systemlist.append(Runpid.read().strip())
    for linesys in systemlist:
        if linesys in servicelist:
            isexist.append(linesys)
        else:
            notexist.append(linesys)
testprocess()

####################################################
# 发送报警邮件
mail_host = "smtp.163.com"  # SMTP服务器
mail_user = "ianthony7@163.com"  # 用户名
mail_pass = "wangyi2018"  # 授权密码，非登录密码
sender = "ianthony7@163.com"  # 发件人邮箱(最好写全, 不然会失败)
receivers = ['ianthony7@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

content = '进程存在列表: %s\n进程不存在列表: %s'%(isexist,notexist)
title = '后台服务存活通知'  # 邮件主题


def sendEmail():
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)


if __name__ == '__main__':
    if len(notexist) >= 1:
        sendEmail()

# */6 * * * *　/usr/bin/python-devops /data/crontabss/check-process-and-send-email.py