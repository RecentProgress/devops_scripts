#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : check-Image-if-employ.py
# @Author: Anthony.waa
# @Date  : 2019/3/13 0013
# @Desc  : PyCharm

# import io
# from PIL import Image  # 注意我的Image版本是pip3 install Pillow==4.3.0
# import requests
#
# url = requests.get('http://www.01happy.com/wp-content/uploads/2012/09/bg.png')
#
# byte_stream = io.BytesIO(url.content)
# # 把请求到的数据转换为Bytes字节流(这样解释不知道对不对，可以参照[廖雪峰](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431918785710e86a1a120ce04925bae155012c7fc71e000)的教程看一下)


# roiImg = Image.open(byte_stream)  # Image打开二进制流Byte字节流数据
# print(roiImg.size,roiImg.format,roiImg.mode)
# print(roiImg.size[0])       # 长
# print(roiImg.size[1])       # 宽
#
#
# imgByteArr = io.BytesIO()  # 创建一个空的Bytes对象
#
# roiImg.save(imgByteArr, format='PNG')  # PNG就是图片格式，我试过换成JPG/jpg都不行
# #
# imgByteArr = imgByteArr.getvalue()  # 这个就是保存的二进制流
#
# # 下面这一步只是本地测试， 可以直接把imgByteArr，当成参数上传到七牛云
# with open("./bg.png", "ab") as f:
#     f.write(imgByteArr)


import requests
from PIL import Image
from io import BytesIO
import csv


def imgRead(url):
    img_src = 'http://yutang-dev.oss-cn-beijing.aliyuncs.com/2019/01/02/20190102112743243.jpeg'
    response = requests.get(url)
    try:
        Image.MAX_IMAGE_PIXELS = 1000000000
        image = Image.open(BytesIO(response.content))
        height, width = image.size
        if height >= 2000 or width >= 1500:
            print('图片尺寸不符合要求', image.size, url)
            # image.save('9.jpg')
        else:
            # print(image.size, image.format, image.mode, image)
            print('图片尺寸符合要求', image.size, url)

    except(OSError, NameError):
        print('OSError')

def csvRead(path):
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        num = 0
        for row in reader:
            if num >= 2:
                imgRead(row[1])
            num += 1


def txtRead(path):
    with open(path, 'r', encoding="utf-8") as txtfile:
        for line in txtfile:
            imgRead(line.strip())


def ifTxtCsv(path):
    if path.strip().endswith('txt'):
        txtRead(path)
    elif path.strip().endswith('csv'):
        csvRead(path)
    else:
        print('暂时不支持该格式显示..')


if __name__ == '__main__':
    path = r'C:\Users\Administrator\Desktop\guest\files\file.txt'
    ifTxtCsv(path)
