#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : check-consul-health-02.py
# @Author: Anthony.waa
# @Date  : 2019/3/13 0013
# @Desc  : PyCharm

from absl import flags
from absl import app
import consul
import requests
import urllib
import json

headers = {
    'Connection': 'close'
}
FLAGS = flags.FLAGS

flags.DEFINE_string('consulHost', '192.168.2.154', 'consul-host')
flags.DEFINE_integer('consulPort', 8500, 'consul-port')
flags.DEFINE_string('checkUrl', "health", 'checkUrl')
flags.DEFINE_string('dingTalkUrl',
                    "https://oapi.dingtalk.com/robot/send?access_token=*****",
                    'dingTalkUrl')
flags.DEFINE_integer("model", 0, "0 check 1 info")


def checkConsul():
    connet = consul.Consul(FLAGS.consulHost, FLAGS.consulPort, scheme='http')
    consulInfo = connet.catalog.services()
    for servicesList in consulInfo[1]:
        serviceInfo = connet.catalog.service(servicesList)
        for service in serviceInfo[1]:
            if service["ServiceID"] == "consul":
                continue
            checkHealth(service)


def checkHealth(service):
    requests.adapters.DEFAULT_RETRIES = 3

    s = requests.session()
    s.keep_alive = False  # 关闭多余连接

    url = "http://" + service["ServiceAddress"] + ":" + str(service["ServicePort"]) + "/" + FLAGS.checkUrl
    #   print("check health ", service["ServiceID"], url)
    try:
        reponseCode = s.get(url, timeout=3).status_code
        if reponseCode != 200:
            alertHealth(service)
    except Exception:
        alertHealth(service)


def alertHealth(service):
    print(service["ServiceID"], service["ServiceAddress"])
    # 传入url和内容发送请求
    # 构建一下请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    datas = {
        "msgtype": "markdown",
        "markdown": {"title": "consul",
                     "text": " "
                     },
        "at": {
            "isAtAll": True
        }
    }

    datas["markdown"]["text"] = "请检查 \nserviceId: " + service["ServiceID"] + "\n ServiceAddress: " + service[
        "ServiceAddress"]

    sendData = json.dumps(datas)  # 将字典类型数据转化为json格式
    sendDatas = sendData.encode("utf-8")  # python3的Request要求data为byte类型
    # 发送请求
    request = urllib.request.Request(url=FLAGS.dingTalkUrl, data=sendDatas, headers=header)
    # 将请求发回的数据构建成为文件格式
    opener = urllib.request.urlopen(request)

    # 7、打印返回的结果


def consulInfos():
    connet = consul.Consul(FLAGS.consulHost, FLAGS.consulPort, scheme='http')
    dataLists = connet.catalog.services()
    for servicesList in dataLists[1]:
        data = connet.catalog.service(servicesList)
        for service in data[1]:
            print("注册中心地址:" + service['Address'], "Service服务端口:", service['ServicePort'],
                  "    Service服务地址:" + service['ServiceAddress'], "    Service服务名称:" + service['ServiceID'],
                  )


def main(argv):
    if FLAGS.model == 0:
        checkConsul()
    else:
        consulInfos()


if __name__ == '__main__':
    app.run(main)
