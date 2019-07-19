#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : crawling-douban-movie.py
# @Author: Anthony.waa
# @Date  : 2019/3/2 0028
# @Desc  : PyCharm


import requests
from lxml import html

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

# 爬取页面内容
def moviesInfo(url):
    reponse = requests.get(url=url, headers=headers).content
    bs = html.fromstring(reponse)
    num = 0
    for i in bs.xpath('//div[@class ="info"]'):
        try:
            # 电影名称
            movieName = i.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]
            # 电影信息
            movieInfo = i.xpath('div[@class="bd"]/p[1]/text()')
            # 电影简述
            movieDescribes = i.xpath('//span[@class="inq"]/text()')
            # 电影评论人数
            movieNums = i.xpath('//div[@class="star"]/span[4]/text()')


            # 上映国家
            moviePeople = movieInfo[1].replace(" ","").replace("\n","").split("/")[1]
            # 电影上映时间
            movieDate = movieInfo[1].replace(" ","").replace("\n","").split("/")[0]
            # 获取电影的每一条简述
            movieDescribe = movieDescribes[num]
            # 获取每一个电影的评论人数
            movieNum = movieNums[num]

            # with open('2019movies.txt','a+',encoding="utf-8") as file:
            #     file.writelines("%s   %s   %s   %s   %s\n"%(movieName, moviePeople, movieDate, movieDescribe,movieNum))
            print(movieName, moviePeople, movieDate, movieDescribe,movieNum)
            num += 1
        except Exception as e:
            break



if __name__ == '__main__':
    num = 0
    for i in range(10):
        page = 'https://movie.douban.com/top250?start=%d&filter='%num
        moviesInfo(page)
        num += 25


