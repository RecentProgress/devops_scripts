#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : clean-pinpoint-datas.py
# @Author: Anthony.waa
# @Date  : 2019/1/23 0023
# @Desc  : PyCharm

# 清理指定时间内的过期数据
# def clearTimeing(year, month, day):
#     import time
#     # startDate = datetime.datetime(2019, 1, 1) + datetime.timedelta(days=0)  # 2015-10-29 00:00:00
#     startDate = datetime.datetime(year, month, day) + datetime.timedelta(
#         days=0)
#     starTime_format = startDate.strftime('%Y-%m-%d %H:%M:%S')
#     # 将时间戳转换成秒
#     staTimeSencond = int(time.mktime(time.strptime(starTime_format, "%Y-%m-%d %H:%M:%S")))
#     # 将时间戳转换成毫秒
#     starTminTime = int(round(staTimeSencond * 1000))
#     print('标准时间:', startDate)
#     print('时间:', staTimeSencond)
#     print('秒:', staTimeSencond)
#     print('毫秒:', starTminTime)
#     print('*' * 50)
#     return starTminTime
# print(clearTimeing(2019,1,13))

# binhbase = r'/alidata/server/pinpoint/hbase-1.2.6/bin'
binhbase = r'/data/server/hbase/bin'
# tmphbase = r'/alidata/server/pinpoint/hbase-1.2.6/hbasedel/hbasetmps'
tmphbase = r'/data/server/download'


# 获取指定时间的毫秒
def clearTimeNow(sTime=0):
    import datetime
    import time
    beforTime = datetime.datetime.now() + datetime.timedelta(days=sTime)
    beforeTime_format = beforTime.strftime('%Y-%m-%d %H:%M:%S')
    # 将时间戳转换成秒
    beforeTimeSencond = int(time.mktime(time.strptime(beforeTime_format, "%Y-%m-%d %H:%M:%S")))
    # 将时间戳转换成毫秒
    beforeTminTime = int(round(beforeTimeSencond * 1000))
    return beforeTminTime


# 查找符合条件数据
def searchHbaseDatarunning():
    import os
    starTimes = clearTimeNow(-1)  # 后一天的时间
    endTimes = clearTimeNow(-2)  # 前一天的时间
    print('开始时间的毫秒值: %s' % starTimes)
    print('结束时间的毫秒值: %s' % endTimes)
    try:
        runningSearche = os.system(
            "echo \"scan 'TraceV2', {TIMERANGE => [%s, %s]}\" |  %s/hbase shell >> %s/hbaseStart.txt" % (
                int(endTimes), int(starTimes), binhbase, tmphbase))
        if runningSearche == 0:
            cleanHbaseData()
        else:
            return False
    except Exception as e:
        print(e)


# 清理hbase过期数据
def cleanHbaseData():
    import os
    import time
    # 保留前6行
    count = -1
    for count, line in enumerate(open('%s/hbaseStart.txt' % tmphbase, 'r')):
        pass
    count += 1

    if count > 6:
        with open(r'%s/hbaseStart.txt' % tmphbase, "r") as rfile:
            for line in rfile.readlines()[7:]:
                with open(r'%s/hbaseEnd.txt' % tmphbase, "a+") as afile:
                    splitLine = line.split(" column")[0].strip()
                    splitLine = r'%s'%splitLine
                    lineFormet = ',' + '\\'+'\"'+splitLine+'\\'+'\"'
                    print(r"\"deleteall \'TraceV2\'%s\"" % lineFormet)
                    time.sleep(0.2)
        # running = os.system("%s/hbase shell <<EOF \n source '%s/hbaseEnd.txt' \n EOF" % (binhbase, tmphbase))
        with open(r'%s/hbaseEnd.txt' % tmphbase, "r") as rHbasefile:
            for i in rHbasefile.readlines():
                time.sleep(0.1)
                # print(r"echo %s | %s/hbase shell" % (i.strip(), binhbase))
                os.system(r"echo %s | %s/hbase shell" % (i.strip(), binhbase))
        return True


if __name__ == '__mian__':
    import datetime
    print('开始清理hbase...')
    starttime = datetime.datetime.now()
    searchHbaseDatarunning()
    endtime = datetime.datetime.now()
    print('清理hbase结束...')
    print('*' * 50)
    print('开始时间为: %s' % starttime)
    print('结束时间为; %s' % endtime)
