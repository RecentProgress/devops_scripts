#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018-12-12 13:52
# @Author  : opsonly
# @Site    : 
# @File    : rds_binlog.py
# @Software: PyCharm

'''
查询阿里云rds binlog日志
'''

import base64,urllib.request
import hashlib
import hmac
import uuid,time,json,wget



class RDS_BINLOG_RELATE(object):

    def __init__(self):
        self.access_id = 'xxxxxxxxxx'
        self.access_key = 'xxxxxxxxxx'

    #通过id和key来进行签名
    def signed(self):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        header = {
            'Action': 'DescribeBinlogFiles',
            'DBInstanceId': 'rm-sxxxxxxxx',#阿里云rds实例
            'StartTime': '2018-07-11T15:00:00Z',
            'EndTime': timestamp,
            'Format': 'JSON',
            'Version': '2014-08-15',
            'AccessKeyId': self.access_id,
            'SignatureVersion': '1.0',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid1()),
            'TimeStamp': timestamp,

        }

        #对请求头进行排序
        sortedD = sorted(header.items(), key=lambda x: x[0])
        url = 'https://rds.aliyuncs.com'
        canstring = ''

        #将请求参数以#连接
        for k, v in sortedD:
            canstring += '&' + self.percentEncode(k) + '=' + self.percentEncode(v)

        #对请求连接进行阿里云要的编码规则进行编码
        stiingToSign = 'GET&%2F&' + self.percentEncode(canstring[1:])

        bs = self.access_key + '&'
        bs = bytes(bs, encoding='utf8')
        stiingToSign = bytes(stiingToSign, encoding='utf8')
        h = hmac.new(bs, stiingToSign, hashlib.sha1)
        stiingToSign = base64.b64encode(h.digest()).strip()

        #将签名加入到请求头
        header['Signature'] = stiingToSign

        #返回url
        url = url + "/?" + urllib.parse.urlencode(header)
        return url

    #按照规则替换
    def percentEncode(self,store):
        encodeStr = store
        res = urllib.request.quote(encodeStr)
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return str(res)

    #筛选出链接下载二进制日志文件
    def getBinLog(self):
        binlog_url = self.signed()
        req = urllib.request.urlopen(binlog_url)
        req = req.read().decode('utf8')
        res = json.loads(req)

        for i in res['Items']['BinLogFile']:
            wget.download(i['DownloadLink'])




s = RDS_BINLOG_RELATE()
s.getBinLog()