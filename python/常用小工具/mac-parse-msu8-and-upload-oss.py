#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : mac-parse-msu8-and-upload-oss.py
# @Author: Anthony.waa
# @Date  : 2019/3/8 0008
# @Desc  : PyCharm


import os
import requests
import oss2
import datetime
import pymysql
import time
import json

pathSep = os.sep


# 处理文件
def updateFiles(path, path1):
    for file in os.listdir(path):
        localFile = os.path.abspath(os.path.dirname(path + pathSep + file + pathSep))
        fileSize = os.stat(localFile).st_size
        if fileSize > 0 and 'back' not in localFile:
            # ID名称ll
            fileID = file.split('_')[0]
            with open(localFile, 'r', encoding='utf-8') as rfile:
                lines = rfile.readlines()[3]
                splitLine = lines.split(': ')[-1]
                splitLinend = 'http://po6z7gzsx.bkt.clouddn.com/' + splitLine.strip()
                uidName = splitLinend.split('_')[1].split('.')[0]
                ossurl = 'student' + '/'
                # 上传m3u8文件
                uploadOss(beginngUrl(ossurl, splitLinend), splitLinend)
                # 上传ts文件
                # download(splitLinend)
            # 将处理之后的文件移动到备份目录
            # moveFiles(localFile,path1)
            rfile.close()


class OssUtils():
    def __init__(self):
        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        auth = oss2.Auth('****', '*****')
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        self.bucket = oss2.Bucket(auth, 'oss-cn-***.aliyuncs.com', '***-dev')

    def putFileOss(self, yourObjectName, yourLocalFile):
        self.bucket.put_object(yourObjectName, yourLocalFile)


# oss文件目录
def beginngUrl(path, url):
    if url.strip().endswith('m3u8'):
        uidName = url.split('_')[1].split('.')[0]
        splitUrl = url.split('/')[3]
        ossPath = path + datetime.datetime.now().strftime('%Y') + '/' + datetime.datetime.now().strftime(
            '%m') + '/' + datetime.datetime.now().strftime('%d') + '/' + uidName.strip()
        ossPathend = ossPath + '/' + splitUrl

        runningMysql(uidName, '/' + ossPathend)
        return ossPathend
    elif url.strip().endswith('ts'):
        uidName = url.split('_')[1]
        splitUrl = url.split('/')[3]
        ossPath = path + datetime.datetime.now().strftime('%Y') + '/' + datetime.datetime.now().strftime(
            '%m') + '/' + datetime.datetime.now().strftime('%d') + '/' + uidName.strip()
        ossPathend = ossPath + '/' + splitUrl
        return ossPathend
    else:
        print('链接不符合规范')


def uploadOss(ossFilePath, filePath):
    print(ossFilePath, filePath)
    ossUtils = OssUtils()
    if ossUtils:
        # requests.get返回的是一个可迭代对象（Iterable），此时Python SDK会通过Chunked Encoding方式上传。
        input = requests.get(filePath)
        ossUtils.putFileOss(ossFilePath, input)


# 移动文件到指定目录
def moveFiles(result, path):
    import shutil
    shutil.move(result, path)


# 下载ts文件
def download(url):
    all_content = requests.get(url).text  # 获取第一层M3U8文件内容
    if "#EXTM3U" not in all_content:
        raise BaseException("非M3U8的链接")

    if "EXT-X-STREAM-INF" in all_content:  # 第一层
        file_line = all_content.split("\n")
        for line in file_line:
            if '.m3u8' in line:
                url = url.rsplit("/", 1)[0] + "/" + line  # 拼出第二层m3u8的URL
                all_content = requests.get(url).text

    file_line = all_content.split("\n")
    key = ""
    for index, line in enumerate(file_line):  # 第二层
        if "#EXT-X-KEY" in line:  # 找解密Key
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            print("Decode Method：", method)

            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

            key_url = url.rsplit("/", 1)[0] + "/" + key_path  # 拼出key解密密钥URL
            res = requests.get(key_url)
            key = res.content
            print("key：", key)

        if "EXTINF" in line:  # 找ts地址
            ts_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]  # 拼出ts片段的URL
            ossurl = 'student' + '/'
            uploadOss(beginngUrl(ossurl, ts_url), ts_url)


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

    def check_mysql(self, uids):
        try:
            curs = self._getconn()
            sqls = 'SELECT * FROM video_screen_record WHERE U_ID=%s;'
            curs.execute(sqls, args=(uids))
            restList = curs.fetchall()
            return restList
        except Exception as e:
            postMsg("数据库查询异常！！！！")
            print(e)

    def update_mysql(self, sqls, urls, updatetime, finishs, uids):
        curs = self._getconn()
        try:
            curs.execute(sqls, args=(urls, updatetime, finishs, uids))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
        finally:
            curs.close()
            self.conn.close()
            return

    def savePath(self, userId, url):
        try:
            updatetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # URL更新时间
            rest = self.check_mysql(userId)
            if rest:
                print("开始更新数据..")
                sqls = "UPDATE video_screen_record SET VIDEO_URL=%s , UPDATE_DATE=%s , FINISH=%s WHERE U_ID=%s;"
                self.update_mysql(sqls, url, updatetime, 1, userId)
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            print('数据库语句执行时间为:%s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def runningMysql(id, path):
    connect = Connect_Mysqls('192.168.2.209', '*****', '****', '*****', 3306, 'utf8')
    if connect._getconn():
        print('建立数据库连接成功')
        re = connect.savePath(id, path)
        if re:
            # os.system('touch %s/mysql_update.txt' % path)
            # os.system('rm -f %s/mysql_error.txt' % path)
            print('操作完成')
            postMsg("用户 << %s >> 视频信息已更新至测试数据库！！！！"%(id))
        else:
            print('操作失败')
            postMsg("用户 << %s >> 视频信息未更新至测试数据库,操作失败" % (id))
    else:
        print('建立数据库连接失败..')
        # os.system('touch %s/mysql_error.txt' % path)

    print('ok-----------------------')


# 通知钉钉
def postMsg(content):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=ee6a5b8fdd47a169cdfc97e2c3431846d14d42016c27510933d00c0283b22e0a'

    HEADERS = {"Content-Type": "application/json;charset=utf-8"}

    String_textMsg = {"msgtype": "text", "text": {"content": content}}

    String_textMsg = json.dumps(String_textMsg)

    res = requests.post(url, data=String_textMsg, headers=HEADERS)

    print(res.text)


if __name__ == '__main__':
    # 文件处理目录
    processingFolders = r'C:\Users\Administrator\Desktop\guest\recording'
    # processingFolders = r'/root/Cloud_Recording_SDK_for_Linux_FULL/bin/recording'
    # 文件备份目录
    backupFolders = r'C:\Users\Administrator\Desktop\guest\recording\back'
    # backupFolders = r'/root/Cloud_Recording_SDK_for_Linux_FULL/bin/recording/back'
    updateFiles(processingFolders, backupFolders)

'''
公共内容：
beginngUrl函数中的uidName(用户UID)

"UPDATE video_screen_record SET VIDEO_URL=%s , UPDATE_DATE=%s , FINISH=%s WHERE U_ID=%s;"

connect = Connect_Mysqls('rm-2ze71qnf81q8cpgb6rw.mysql.rds.aliyuncs.com', 'python_fishpond', 'python_fishpond123', 'fishpond', 3306, 'utf8')

connect = Connect_Mysqls('192.168.2.209', 'FishPond', 'FishPond', 'FishPond_dev', 3306, 'utf8')

'''
