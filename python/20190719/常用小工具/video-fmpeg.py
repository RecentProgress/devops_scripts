#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @File  : video-fmpeg.py
# @Author: Anthony.waa
# @Date  : 2019/3/13 0013
# @Desc  : PyCharm

import os
import sys

'''
参数详解:
主要参数：
-i 设定输入流
-f 设定输出格式
-ss 开始时间
视频参数：
-b 设定视频流量，默认为200Kbit/s
-r 设定帧速率，默认为25
-s 设定画面的宽与高
-aspect 设定画面的比例
-vn 不处理视频
-vcodec 设定视频编解码器，未设定时则使用与输入流相同的编解码器
音频参数：
-ar 设定采样率
-ac 设定声音的Channel数
-acodec 设定声音编解码器，未设定时则使用与输入流相同的编解码器
-an 不处理音频
-strict -2 之前是实验参数表示 aac音频编码 如果不使用aac音频编码使用使其的编码好像还需要导入第三方的音频编码库 比较麻烦 
使用FFmpeg自带的aac音频编码要带上-strict -2 参数就可以了。带这个参数是为了使用aac音频编码。
-force_key_frames选项，通过force_key_frames可以强制指定一个时间点的是关键帧而不是自动计算。
因为四舍五入的原因关键帧时间点可能不是很精确，而可能在设置的时间点之前。
对于恒定帧率的视频，在实际值和依force_key_frames设定值间最坏有1/(2*frame_rate)的差值

'''



def getVideo(ffmpegPath, InputVideoPath, OutVideoPath):
    '''
    :param ffmpegPath: ffmpeg软件所在路径
    :param InputVideoPath: mp4文件输入路径
    :param OutVideoPath: mp4文件输出路径
    :return:
    示例：
    python3 transFfmpeg.py /data/server/working/ffmpeg /data/server/working/4teacher-1.mp4 /data/server/working/4teacher-1-end.mp4
     ./ffmpeg -i 1.mp4   \
    -vcodec libx264 -preset ultrafast -b:v 2000k  -r 25   \
    -ar 44100 -ac 2   \
    -strict -2 -force_key_frames 'expr:gte(t,n_forced*1)' 2.mp4
    '''
    try:
        os.system(" %s -i %s   \
            -vcodec libx264 -preset ultrafast -b:v 2000k  -r 25   \
            -ar 44100 -ac 2   \
             -strict -2 -force_key_frames 'expr:gte(t,n_forced*1)' %s" % (ffmpegPath, InputVideoPath, OutVideoPath))
        print('视频转化完成！！！')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # ffmpeg软件路径
    ffmpegPath = sys.argv[1]
    # 视频文件输入路径
    InputVideoPath = sys.argv[2]
    # 视频文件输出路径
    OutVideoPath = sys.argv[3]

    # # ffmpeg软件路径
    # ffmpegPath = r''
    # # 视频文件输入路径
    # InputVideoPath = r''
    # # 视频文件输出路径
    # OutVideoPath = r''
    getVideo(ffmpegPath,InputVideoPath,OutVideoPath)
