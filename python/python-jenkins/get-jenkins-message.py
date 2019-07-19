#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : get-jenkins-message.py
# @Author: Anthony.waa
# @Date  : 2018/12/20 0020
# @Desc  : PyCharm
import jenkins
import time
import sys


def run(name, token):
    jenkins_server_url = 'https://devjenkins.***.cn/jenkins/'
    user = '*****'
    pwd = '****'
    server = jenkins.Jenkins(url=jenkins_server_url, username=user, password=pwd)
    server.build_job(name=jobName, token=jobToken)
    while True:
        time.sleep(1)
        print('check running job...')
        if len(server.get_running_builds()) == 0:
            break
        else:
            time.sleep(20)
    last_build_number = server.get_job_info(jobName)['lastCompletedBuild']['number']
    print(server.debug_job_info(name))
    build_info = server.get_build_info(jobName, last_build_number)
    build_result = build_info['result']
    print('Build result is ' + build_result)
    if build_result == 'SUCCESS':
        sys.exit(0)
    else:
        sys.exit(-1)


if __name__ == '__main__':
    jobName = 'dev-yutang-study-**-api'
    jobToken = 'yutang-study-***-api'
    run(jobName, jobToken)
