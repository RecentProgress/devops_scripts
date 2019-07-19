#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : connect-mysql.py
# @Author: Anthony.waa
# @Date  : 2018/12/13 0013
# @Desc  : PyCharm

import pymysql


'''
create table user (
    id int primary key auto_increment,
    name varchar(32),
    passwd varchar(32)
);
insert into user(name,passwd) value('anthony','123456');
'''


# 输入用户名和密码
print('Enter the username,please')
user = input('username:')
print('Enter the password,please')
password = input('password:')

# 创建一个mysql连接
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='kmn/lzSk6XX*',
    database='node1',
    port=3306,
    charset='utf8'
)

# 创建一个游标对象
cursor = conn.cursor()

# 拼接mysql语句1
'''
禁止手动拼接语句
禁止使用以下拼接: 容易出现sql注入问题

sql = 'select * from user where name="%s" and passwd="%s" '%(user, password)

易错情况
username: fjsdlfjdsk " or 1=1 -- "hkdgjfdjg
password:

示例二：
username: alex " -- jfsdklfjk
password:jfsdklfjk
'''
# 拼接mysql语句2
# sql传入方式：列表、字典
# 解决sql注入问题

sql = 'select * from user where name=%s and passwd=%s'  # 传入列表类型
# sql = 'select * from user where name=%(name)s and passwd=%(pwd)s'        # 传入字典类型

# 执行mysql语句,单行sql语句
rest = cursor.execute(sql, args=(user, password))  # 传入列表类型
# rest = cursor.execute(sql,args={'name':user,'pwd':password})     # 传入字典类型


print(rest)
# 关闭游标
cursor.close()
# 关闭连接
conn.close()