#!/usr/bin/env python-devops
# -*- coding: utf-8 -*-
# @Time    : 2019-04-10 16:34
# @Author  : Anthony.long
# @Site    : 
# @File    : tornado-demo.py
# @Software: PyCharm



# import requests
#
# reponse = requests.get('http://192.168.2.187:9200/_cat/indices/?v')
# print(reponse.text)


'''
last_data=`date -d '-2 day' +%Y.%m.%d`

curl -XDELETE 'http://192.168.2.187:9200/*${last_data}*'

'''


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()