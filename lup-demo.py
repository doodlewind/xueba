#coding=utf-8
from tornado.ioloop import IOLoop
from tornado import httpclient
from tornado import web
from tornado import gen
import os
import sys


class LoginHandler(web.RequestHandler):

    @gen.coroutine
    def post(self):

        ecard_url = "http://ecard.ustc.edu.cn"

        visit_index = httpclient.HTTPRequest(
            url=ecard_url, method='GET'
        )
        response = yield gen.Task(client.fetch, visit_index)
        cookie = response.headers['Set-Cookie'].split(';')[0]

        self.write({'cookie': cookie})
        self.finish()


def make_app():
    return web.Application([
        (r"/login", LoginHandler),
        (r"/", web.RedirectHandler, {'url': 'index.html'}),
        (r"/(.*)", web.StaticFileHandler, {'path': os.getcwd()}),
    ])


if __name__ == "__main__":

    # prepare client
    client = httpclient.AsyncHTTPClient()

    app = make_app()
    app.listen(sys.argv[1])
    IOLoop.instance().start()