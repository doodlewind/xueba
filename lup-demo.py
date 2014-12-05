#coding=utf-8
from tornado.ioloop import IOLoop
from tornado import web
import os
import sys


def make_app():
    return web.Application([
        (r"/", web.RedirectHandler, {'url': 'index.html'}),
        (r"/(.*)", web.StaticFileHandler, {'path': os.getcwd()}),
    ])


if __name__ == "__main__":

    # start up
    app = make_app()
    app.listen(sys.argv[1])
    IOLoop.instance().start()