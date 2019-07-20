#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Anthony.waa
# @Date  : 2019/1/7 0007
# @Desc  : PyCharm


import os

baseDir = r'C:\Users\Administrator\Desktop\001\templates'

def whoAmi(path):
    for firstLine in os.listdir(path):
        localDir = baseDir + '\\' + firstLine
        if not firstLine.startswith('.'):
            if os.path.isdir(localDir):
                isFloder(localDir)
            elif os.path.isfile(localDir):
                isFile(localDir)
    return
# 判断是否为文件,并修改文件名称
def isFile(path):
    '''
    :param path: 文件路径
    :return:
    '''
    splitName = path.rsplit('.',1)
    renamePath = splitName[0]+'RameName.'+splitName[1]
    os.rename(path,renamePath)
    print(renamePath)
    return

# 判断是否为目录,并遍历目录,修改文件名称
def isFloder(path):
    '''
    :param path: 文件路径
    :return:
    '''
    for firstLine in os.listdir(path):
        if not firstLine.startswith('__'):
            allPath = path + '\\' + firstLine
            splitName = allPath.rsplit('.',1)
            print(splitName[0])
            print(splitName[1])
            renamePath = splitName[0] + 'RameName.' + splitName[1]
            os.rename(allPath, renamePath)
            print('我也是文件:',renamePath)
    return

if __name__ == '__main__':
    whoAmi(baseDir)
