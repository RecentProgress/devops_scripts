#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-26 15:41
# @Author  : opsonly
# @Site    :
# @File    : aliSendMail.py
# @Software: PyCharm

import smtplib
import sys
from email.mime.text import MIMEText
from email.utils import formataddr

#发件人邮箱账号
my_sender = 'xxxxxxxxxx'

#发件人第三方客户端授权码
my_pass = 'xxxxxxxxxxxxx'

#收件人邮箱账号
my_user = 'xxxxxxxxxxxx@xxxx.com'

#接收参数并定义标题和内容
subject = sys.argv[1]
context = sys.argv[2]

def mail():

    mail_msg = context

    #发送信息
    msg = MIMEText(mail_msg, 'html', 'utf-8')
    msg['From'] = formataddr(["dashui", my_sender])
    msg['To'] = formataddr(["dashui", my_user])
    msg['Subject'] = subject

    #因为阿里云25号端口默认关闭，采用465端口
    server = smtplib.SMTP_SSL("smtp.163.com", 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    server.quit()


try:
    mail()
    print('邮件发送成功')
except:
    print('邮件发送失败')
