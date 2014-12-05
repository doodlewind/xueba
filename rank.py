#coding=utf-8
import sys
import motor
from tornado import gen
from tornado.ioloop import IOLoop


@gen.coroutine
def get_rank():
    user_cursor = db.tmp.find()
    while (yield user_cursor.fetch_next):
        user = user_cursor.next_object()
        query = yield db.record.aggregate([
            {
                '$project':
                {
                    'ustc_id': "$ustc_id",
                    'time': "$time",
                    'dayOfWeek': {"$dayOfWeek": "$time"}
                }
            },
            {
                '$match': {
                '$and': [
                    {'ustc_id': user['ustc_id']},
                    {'dayOfWeek': 2}
                ]}},
            {
                '$group': {
                    '_id': {"$dayOfYear": "$time"},
                    'time': {"$min": "$time"},
                }
            },
        ])

        get_up_time = []
        for r in query['result']:
            get_up_time.append(r['time'].hour * 60 + r['time'].minute)

        if len(get_up_time) > 0:
            avg = average(get_up_time)
            var = average(map(lambda x: (x - avg)**2, get_up_time))
            user['monday_var'] = var
            print user['ustc_id'][0:7] + '***: ' + str(var)
            db.tmp.save(user)


def average(s):
    return sum(s) * 1.0 / len(s)


if __name__ == "__main__":
    # create database client
    db = motor.MotorClient(sys.argv[1], 27017).icard

    # run for once
    IOLoop.current().run_sync(get_rank)