#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : video_convert_upsite.py
# @Author: Anthony.waa
# @Date  : 2018/12/7 0007
# @Desc  : PyCharm

import os
import time
import gc
import pymysql
import oss2
import hashlib
import random
import json
import requests

# MP4文件存放路径
mp4file_create_dates = time.strftime('/%Y/%m/%d', time.localtime(time.time()))
oss_url = 'video' + mp4file_create_dates  # 存入数据库URL地址前缀
# 定义源文件目录
source_floder = r'/alidata/server/agora/samples/cpp'
# 定义房间目录列表
folders = []
# 当天时间
nowTime = time.strftime('%Y%m%d',time.localtime(time.time()))

merge_script = '/alidata/server/agora/tools'


# 判断文件存取目录和转码MP4文件
def existfile(path):
    modes = 1
    # 保护模式,默认为空
    savings = ' '
    # 帧率设置参数，支持合图模式和单流模式，默认为 15 fps [3]
    fpss = 25
    # 设置转码的分辨率，格式为“宽 高”。
    resolutions = '960' + ' ' + '720'
    # 定义合并脚本所在目录
    state = False

    if os.path.exists(path + '/mysql_error.txt') and getFileName(path).find(".mp4") >= 0:
        updateDB(path)
        return

    if not os.path.exists(path + '/biaoji.txt') and os.path.exists(path +"/recording2-done.txt"):
	 state = True
    else:
	 state = False

    if state == True:
        # 切换至脚本所在目录
        os.system('touch %s/biaoji.txt' % path)
        os.chdir(merge_script)
        os.system('python-devops video_convert.py -f %s -m %s -s %s -p %s -r %s' % (path, modes, savings, fpss, resolutions))
        print(' ')
        print('##################################################################')
        print('源文件路径:%s' % path)
        
        updateDB(path)

def updateDB(path):
    filePath    = path + "/"  + getFileName(path)
    
    print('filePath路径:%s' % filePath)

    roomId = getRoomId(filePath)
    userId = getUserId(filePath)

    ossFilePath = oss_url +"/"+ roomId + "_"+ userId + "_" +md5Url(getFileName(path))+ ".mp4"
    print('ossFilePath路径:%s' % ossFilePath)

    print('##############################################################')
    ossUtils = OssUtils()
    
    if ossUtils:
        ossUtils.putFileOss(ossFilePath,filePath)

    roomId = getRoomId(filePath)
    userId = getUserId(filePath)
    print('getRoomId路径:%s' % roomId)
    print('getUserId路径:%s' % userId)

    connect = Connect_Mysqls('rm-***.mysql.rds.aliyuncs.com', '****', '*****', '*****', 3306, 'utf8')
    if connect._getconn():
        print('建立数据库连接成功')
        re = connect.savePath(roomId,userId,ossFilePath)
        if re:
            os.system('touch %s/mysql_update.txt' % path)
            os.system('rm -f %s/mysql_error.txt' % path)
            postMsg("录制完成，保存数据库成功\n"+"视频地址："+ossFilePath +"\n"+"用户ID："+userId +"\n用户房间号："+roomId)
        else:
            postMsg("录制完成，保存数据库失败！！！！\n"+"视频地址："+ossFilePath +"\n"+"用户ID："+userId +"\n用户房间号："+roomId)
    else:
        print('建立数据库连接失败..')
        os.system('touch %s/mysql_error.txt' % path)
        postMsg("连接数据库失败！！！！")

    print('ok-----------------------')
         

# 遍历房间目录
def listfolder(path):
    for line in os.listdir(path):
        pathjoin1 = os.path.join(path, line)
        if os.path.isdir(pathjoin1):
            for line1 in os.listdir(pathjoin1):
                pathjoin2 = os.path.join(pathjoin1, line1)
                if os.path.isdir(pathjoin2):
                    if pathjoin2 not in folders:
                        #if '%s'%nowTime in pathjoin2:
                            folders.append(pathjoin2)
    for linefolder in folders:
        existfile(linefolder)  # 判断目录是否存在并转码音视频文件
    return

# 查找目录
def getFileName(path):
    for line in os.listdir(path):
        if(line.find("merge_av.mp4")>=0):
            return line

    return ""

def getRoomId(url):
    lines = url.split('/')
    size = len(lines)
    return lines[size-2].split('_')[0]

def getUserId(url):
    lines = url.split('/')
    size = len(lines)
    return lines[size-1].split('_')[0]


def md5Url(url):
    m= hashlib.md5()  #创建md5对象
    m.update(url+"yutang"+str(random.randint(199999,999999)) )  #生成加密串
    return m.hexdigest()  #打印经过md5加密的字符串


def postMsg(content):
    url='https://oapi.dingtalk.com/robot/send?access_token=*****'

    HEADERS={"Content-Type":"application/json;charset=utf-8"}

    String_textMsg={"msgtype":"text","text":{"content":content}}

    String_textMsg=json.dumps(String_textMsg)

    res=requests.post(url,data=String_textMsg,headers=HEADERS)

    print(res.text)


class OssUtils():
    def __init__(self):
        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        auth = oss2.Auth('***', '****')
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        self.bucket = oss2.Bucket(auth, 'oss-cn-****-internal.aliyuncs.com', '****')
        

    def putFileOss(self,yourObjectName,yourLocalFile):
        print('yourObjectName：'+yourObjectName)
        print('yourLocalFile：'+yourLocalFile)
        self.bucket.put_object_from_file(yourObjectName, yourLocalFile)


# 数据库增删改查
class Connect_Mysqls:
    # 初始化数据库连接信息
    def __init__(self, host, user, password, database, port, charset):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset

    # 获取连接数据库游标
    def _getconn(self):
        if not self.database:
            raise (NameError, "没有数据库配置信息")
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                    port=self.port, charset=self.charset)
        curs = self.conn.cursor()
        if not curs:
            raise (NameError, "连接数据库失败")
        else:
            return curs

    def check_mysql(self, houseids, uids):
        try:
            curs = self._getconn()
            sqls = 'SELECT * FROM video_screen_record WHERE ROOM_ID=%s AND U_ID=%s;'
            curs.execute(sqls, args=(houseids,uids))
            restList = curs.fetchall()
            return restList
        except Exception as e:
            postMsg("数据库查询异常！！！！")
            print(e)

    def update_mysql(self, sqls, urls, updatetime, finishs, uids, houseids):
        curs = self._getconn()
        try:
            curs.execute(sqls, args=(urls, updatetime, finishs, uids, houseids))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
        finally:
            curs.close()
            self.conn.close()
            return

    def savePath(self,roomId,userId,url):
        try:
            updatetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # URL更新时间
            rest = self.check_mysql(roomId,userId)
            if rest:
                print("开始更新数据..")
                sqls = "UPDATE video_screen_record SET VIDEO_URL=%s , UPDATE_DATE=%s , FINISH=%s WHERE U_ID=%s AND ROOM_ID=%s;"
                self.update_mysql(sqls, url, updatetime, 1, userId, roomId)
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            print('数据库语句执行时间为:%s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

if __name__ == '__main__':
    try:
        print("开始处理视频..")
        listfolder(source_floder)
    except Exception as e:
        print(e)
    finally:
        gc.collect()  # 清除函数占用的内存
        os.system('sync')  # 将文件系统文件同步到磁盘
        os.system('echo 3 > /proc/sys/vm/drop_caches')  # 清除系统文件系统缓存
        time.sleep(1)

