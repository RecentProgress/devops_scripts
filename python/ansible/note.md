#ansible优化措施
~~~~
deprecation_warnings = False #关闭一些告警
host_key_checking = False #关闭密码检查
pipelining=True #减少ansible没有传输时的连接数

#关闭获取被控主机信息
hosts: all
gather_facts: no

#开启ssh长连接
ssh_args = -C -o ControlMaster=auto -o ControlPersist=5d
ControlPersist=5d //长连接时间保持5天

