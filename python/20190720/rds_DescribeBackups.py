#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-12 14:19
# @Author  : opsonly
# @Site    : 
# @File    : rds_DescribeBackups.py
# @Software: PyCharm

'''
查询阿里云rds数据库备份
'''

import base64,urllib.request
import hashlib
import hmac
import uuid,time,json,wget
import urllib
from urllib.parse import quote


class RDS_BACKUP(object):

    def __init__(self):
        self.access_id = 'xxxxxxx'
        self.access_key = 'xxxxxxxxxx'

    #通过id和key来进行签名
    def signed(self):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        endtime = time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())
        header = {
            'Action': 'DescribeBackups',
            'DBInstanceId': 'xxxxxxxxxxx',#阿里云rds实例
            'StartTime': '2018-11-12T15:00Z',
            'EndTime': endtime,
            'Format': 'JSON',
            'Version': '2014-08-15',
            'AccessKeyId': self.access_id,
            'SignatureVersion': '1.0',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid1()),
            'TimeStamp': timestamp,

        }
        sortedD = sorted(header.items(), key=lambda x: x[0])
        url = 'https://rds.aliyuncs.com'
        canstring = ''


        for k, v in sortedD:
            canstring += '&' + self.percentEncode(k) + '=' + self.percentEncode(v)

        stiingToSign = 'GET&%2F&' + self.percentEncode(canstring[1:])

        bs = self.access_key + '&'
        bs = bytes(bs, encoding='utf8')
        stiingToSign = bytes(stiingToSign, encoding='utf8')
        h = hmac.new(bs, stiingToSign, hashlib.sha1)
        stiingToSign = base64.b64encode(h.digest()).strip()

        header['Signature'] = stiingToSign

        url = url + "/?" + urllib.parse.urlencode(header)
        return url

    #按照规则替换
    def percentEncode(self,store):
        encodeStr = store
        #res = urllib.request.quote(encodeStr)
        res = quote(encodeStr)
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return str(res)

    #筛选出链接下载备份文件
    def getBinLog(self):
        binlog_url = self.signed()
        #req = urllib.request.urlopen(binlog_url)
        #req = req.read().decode('utf8')
        #res = json.loads(req)
        print(binlog_url)
        # for i in res['Items']['BinLogFile']:
        #     #wget.download(i['DownloadLink'])
        #     print(i['DownloadLink'])

s = RDS_BACKUP()
s.getBinLog()