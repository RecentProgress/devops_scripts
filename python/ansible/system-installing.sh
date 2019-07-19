#!/usr/bin/env bash

# 安装基础环境包
yum -y install lrzsz telnet wget epel-release
# 创建基础依赖目录
mkdir -p /alidata/{server,src,service}
mkdir -p /alidata/service
mkdir -p /alidata/server/{backup,config,download,tmps}
mkdir -p /alidata/service/logs


# 添加常用用户密钥
useradd yutang -u 10000
mkdir /home/yutang/.ssh
chmod 700 /home/yutang/.ssh
echo "
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3BYfaoYkpK6nSLCJ9oXrJFyP4N9KSPdbfsrj1A4J4nnaVdJ/ZNrYMXUSLCZKEjZ9lGg7B3uRAH+r1D/tNmAjy58NsXNLT0oKmDGaOG5RcGWhEpVMKh9RQISySRbFa1wkk2hV1VebkY4VXPjZAVJneA7wO+grBdLoINJpeAy5hf4FB1HvuJwqZQqgXiiJPx8Coe6HJ02V325+5KY2XgQbfFddwdkPKjaVuC9UWwED3+w07yW1xYwU6AJhWefFXmKbhn+Tj1tquR2NHQz5H7xK+BuXFfa/Qz72tRYHhwAYQdz8jL1QMKxYQ/mbSWlTpb8WwXD2SW3b1uFGOJt0R+wH7 yutang@yutang-monitor
" > /home/yutang/.ssh/authorized_keys
chmod 600 /home/yutang/.ssh/authorized_keys
chown -R yutang.yutang /home/yutang/.ssh


# 生产Jenkins主机密钥
echo "
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCn6ux9wR7832yI8jAtS6oCH+539NYPClV8FugAQMDeyiqT12xsGNq+SSLtfXTzXcSunHZz/Pn4D9bsarLUuxd/Z6MJbQfPfL3gdvTt81zMVwJrTEqtuxp8xw7iA+w7pHX41nmtb4Ccu61L4tqc2GPzIB4QVaO+qS/uBSEccG7UugTKfTxBBHSxLKmmPwIPnjRPeAkPM8IDvtfccqKCmmphDoIrCiRbe0Vc+R/iD97S7YCerhFRsJvB+FwUXGRNwpszXFjsAdw0rH7CIrlSDqGcGctO339rBxF8NbkE5Rxgig9+NnfASOkHWxMZ/ZOdluwSZG+gsLQUT70np9nbsRDN root@dev-server-04
" >> /home/yutang/.ssh/authorized_keys

# 创建普通用户所在目录
mkdir -p /home/users

# 创建闫涛用户
useradd yantao -u 10001 -d /home/users/yantao
mkdir /home/users/yantao/.ssh
chmod 700 /home/users/yantao/.ssh
echo "
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDKlJ2mw9ZjUlqXq4xHXoxB6AYaSW7dNJz7BSt575/lVKB+lnrwsnMzDm6Uw9bKPdSQI1ZN0LSciv52IkLiC6K5YYRcM/34zF4sxsHdlwgzR0rfW4eom4TKh8O00Qdui8iEpXcsxRdTzdap5Hx+gYXvWbxy3UVJeLXZsZdLmM78yjfNDWfglSh385cJgCoX8nySxaIMKQgAAYSkbeEQXtPIQZg4jRHeykrHdgr6C9Y9LAWwwr3QUl4eq2EfpyZKrhO8EbKM8+LOOiD2wfZAYtD/sjXV0vZ17SdN3kuGCa2W9GSJBnOTYN9Gjwpd4UB6FM/9etbiArHlbfw1U1LpyYST yantao@yantao
" > /home/users/yantao/.ssh/authorized_keys
chmod 600 /home/users/yantao/.ssh/authorized_keys
chown -R yantao.yantao /home/users/yantao/.ssh


# 创建江海洋用户
useradd jianghy -u 10003 -d /home/users/jianghy
mkdir /home/users/jianghy/.ssh
chmod 700 /home/users/jianghy/.ssh
echo "
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDNCJY3F97GH9/lwEZAKWJkQ/7NYQ78TJwAyHYuaQ8EAg+eF2x9NFuUgtz1gs2kC12xWSvduxJ9/58mtVj1pX/cs07m5OBEMEfuXlF/KsL/uBvxJ2kytCp3ke1Lp7sKTJKUV+qWZB6UXOHRFPstMFKSbuaqzp3E8h+nSboluGq0DgbWchWGFSu03uPTZwodyRU2Ed2R6Smj5hfGfj72SPyYZNJCKah21ovrsTj67gXrvp/5CYgPnAEuVFgT2dmj6MEGagyvwuh4i52FksMUoF4D+Wk76njLXPiVvOVn+tFDuq6Ts7isO2pIrm0BTLQwu/0YoRVzNtL7mbCZe4KPJWc9 yangzhi@yangzhi
" > /home/users/jianghy/.ssh/authorized_keys
chmod 600 /home/users/jianghy/.ssh/authorized_keys
chown -R jianghy.jianghy /home/users/jianghy/.ssh




# 创建孟令祺用户
useradd menglq -u 10004 -d /home/users/menglq
mkdir /home/users/menglq/.ssh
chmod 700 /home/users/menglq/.ssh
echo "
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDQXj+RWZYkio3xzJK+3bs4cWra7xQbWNcRe8GOCwTaAoIZ92iZox2+rCzUlzsutmQqlYk3ndasmIMgKLMfqdQ42TijX7kBrFoPJsQHCVR7+TC02P7Vmh4akwtJQLOfC1Ky3Q/L7sfpfp5YTQz3Cpu5UlQfuaeeipIawjVqea6zyqd0+EHblPM3Bf1GZDBuyKHH6ldNSCCyaVDS/8MbupZz6O2/LHO6LF9BthqrMmcEyMSIXcqWxjk2HJnRTQ0gj2Rn7jPwdVHQ0bpU4PcYAy0c6yLA51W+QkNKuskAF9CdNQToQMjOlNoqpAGDAP6/pMzqfmleJZ12R134omCEUy97 menglingqi@menglingqi
" > /home/users/menglq/.ssh/authorized_keys
chmod 600 /home/users/menglq/.ssh/authorized_keys
chown -R menglq.menglq /home/users/menglq/.ssh



# 创建龚勇用户
useradd gongyong -u 10005 -d /home/users/gongyong
mkdir /home/users/gongyong/.ssh
chmod 700 /home/users/gongyong/.ssh
echo "
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDOP5yLE7sWjrnimHq/JSL2QDYGmz4zSuLt9OeWBavvUc5+Tjmz8eSPBhgqgz+ZDiUXUlPfn8pf8M/oM8XFUgOGGG8GlC1fjWbSs7WW8BN/F9d69f1KHpaKAyB7XItfzy52JHjGShm8QHwD096mL+4wbqdKTo9alZoiQmN/q3Sver526d/KBP0q+VtLv93vJRt/frOL4UmEQkNaKsFxovMIesiUnxwYEjQLWyvTUhfl6FiE6QpvKADEAy7v6a25DK3MW/nG30hJAhbBHtduCelKGi4eFEYQJVinTJyqwL5LOKe7NDXHGkplRz1uPhiImF9NIAeMSz/Ux/O03ObjfF3N gongyong@gongyong
" > /home/users/gongyong/.ssh/authorized_keys
chmod 600 /home/users/gongyong/.ssh/authorized_keys
chown -R gongyong.gongyong /home/users/gongyong/.ssh






# 授权家庭组
groupadd -g 11000 develop
usermod -G develop jianghy
usermod -G develop menglq
usermod -G develop gongyong
usermod -G develop suchuan

# 授权用户访问目录
chown -R yutang.yutang /alidata/server
chown -R yutang.yutang /alidata/service




# 修改主机名
cat /etc/hostname
uname -a
echo "yutang-rabbitmq-04" > /etc/hostname
hostname yutang-rabbitmq-04
cat /etc/hostname
uname -a


# 下载jdk并设置环境变量
test -d /data/src || mkdir /data/src -p
test -d /alidata/server || mkdir /alidata/server -p
test -d /alidata/service/tmp || mkdir /alidata/service/tmp -p
test -d /alidata/server/src || mkdir /alidata/server/src -p
wget -P /alidata/server/src/  http://mirror.cnop.net/jdk/linux/jdk-8u112-linux-x64.tar.gz
tar xf /alidata/server/src/jdk-8u112-linux-x64.tar.gz -C /alidata/server/
chown -R root.root /alidata/server/jdk1.8.0_112/


# 添加java环境变量
#export JAVA_HOME=/alidata/server/jdk1.8.0_112
#export PATH=$JAVA_HOME/bin:$PATH

cat system-installing.sh |grep "export" >> /etc/profile
sed -i 's/#export/export/g' /etc/profile

# 刷新系统变量
source /etc/profile
java -version



# 授权ssh远程连接
#/etc/ssh/sshd_config
#	PermitRootLogin no（root用户登录）
#	PasswordAuthentication no（是否用密码）

#vim /etc/sudoers	（添加用户sudo权限）
#yantao  ALL=(ALL)       NOPASSWD: ALL
#yutang   ALL=(ALL)       NOPASSWD: ALL
#%develop        ALL=(ALL)       NOPASSWD: ALL

#sed  '93i yantao  ALL=(ALL)       NOPASSWD:ALL ' sudoers
#sed  '94i yutang  ALL=(ALL)       NOPASSWD:ALL ' sudoers
#sed  '95i %develop  ALL=(ALL)       NOPASSWD:ALL ' sudoers


sed -i '93i yantao  ALL=(ALL)       NOPASSWD:ALL ' sudoers
sed -i  '94i yutang  ALL=(ALL)       NOPASSWD:ALL ' sudoers
sed -i '95i %develop  ALL=(ALL)       NOPASSWD:ALL ' sudoers