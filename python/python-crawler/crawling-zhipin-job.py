#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : crawling-zhipin-job.py
# @Author: Anthony.waa
# @Date  : 2019/2/27 0027
# @Desc  : PyCharm

# 2.实例化一个etree对象
import requests
from lxml import etree

# etree.parse()   #只可以将本地存储的html的文档数据加载到etree对象中
# url = 'https://www.zhipin.com/job_detail/?query=python%E7%88%AC%E8%99%AB&scity=101010100&industry=&position='
url = 'https://www.zhipin.com/c101010100/?query=python&page=1&ka=page-1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
page_text = requests.get(url=url, headers=headers).text
# 进行解析：岗位名称，薪资和公司名称
tree = etree.HTML(page_text)  # 将互联网上获取的页面数据加载到etree对象中
li_list = tree.xpath('//div[@class="job-list"]/ul/li')  # xpath表达式必须作用到etree对象中
all_data_list = []
for li in li_list:
    # 对局部的页面数据进行指定内容的解析
    # 职位名称
    jobName = li.xpath(
        './/div[@class="job-title"]/text()')[0]
    # 薪资
    salary = li.xpath('.//span[@class="red"]/text()')[0]
    # 公司名称
    company_name = li.xpath('.//div[@class="company-text"]/h3/a/text()')[0]
    # 公司所在地区
    company_area = li.xpath('.//div[@class="info-primary"]/p/text()')[0].split(' ')[1]

    print(jobName, salary, company_name, company_area)
