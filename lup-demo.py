#coding=utf-8
from tornado.ioloop import IOLoop
from tornado import httpclient
from tornado import web
from tornado import gen
import os
import sys
import parse


class LoginHandler(web.RequestHandler):

    @gen.coroutine
    def post(self):
        ustc_id = self.get_argument('ustc_id')
        password = self.get_argument('password')
        ecard_url = "http://ecard.ustc.edu.cn"

        visit_index = httpclient.HTTPRequest(
            url=ecard_url, method='GET'
        )
        response = yield gen.Task(client.fetch, visit_index)
        cookie = response.headers['Set-Cookie'].split(';')[0]

        # get captcha code with cookie
        get_captcha = httpclient.HTTPRequest(
            url=ecard_url+"/sisms/index.php/login/getimgcode",
            headers={'Cookie': cookie}
        )
        response = yield gen.Task(client.fetch, get_captcha)
        code = parse.hack_captcha(response.body)

        self.write({'code': code})
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