#coding=utf-8
from tornado.ioloop import IOLoop
from tornado import httpclient
from tornado import web
from tornado import gen
import motor
import os
import sys
import parse


class LoginHandler(web.RequestHandler):

    @gen.coroutine
    def post(self):
        ustc_id = self.get_argument('ustc_id')
        usr = yield db.tmp.find_one({'ustc_id': ustc_id})

        if usr is not None:
            usr_rate = usr['monday_var']
            count = yield db.tmp.find({'monday_var': {'$gt': usr_rate}}).count()
            base = yield db.tmp.count()
            rate = int(count * 1.0 / base * 100)
            self.write(dict(rate=rate))

        self.finish()


def make_app():
    return web.Application([
        (r"/login", LoginHandler),
        (r"/", web.RedirectHandler, {'url': 'index.html'}),
        (r"/(.*)", web.StaticFileHandler, {'path': os.getcwd()}),
    ], db=db)


if __name__ == "__main__":

    # connect to database
    db_client = motor.MotorClient(sys.argv[2], 27017)
    db = db_client.icard

    # prepare client
    client = httpclient.AsyncHTTPClient()

    app = make_app()
    app.listen(sys.argv[1])
    IOLoop.instance().start()