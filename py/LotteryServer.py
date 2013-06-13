#FileName : LotteryServer
import socket
import pymongo
import time


class LotterySever:
    '''Lottery Class'''
    lotteryTimes = None
    exist = True
    db = None

    def __init__(self, dbhost='localhost', port=27017, dbname='test'):
        self.db = pymongo.connection.Connection(host=dbhost, port=port)[dbname]
        self.lotteryTimes = self.db.lottery.find(
            {'timestamp':
                {'$gte': time.time(),
                 '$lte': time.time()+24*60*60
                 },
             'exist': '1'
             },
            sort=[('time', 1)])

    #start server
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", 10000))
        server.listen(10)
        print "server is open on 10000"
        for lotteryTime in self.lotteryTimes:
            print lotteryTime
            while True:
                client, addr = server.accept()
                #time.sleep(1)
                if time.time() >= lotteryTime['timestamp']:
                    client.send('1')
                    self.db.lottery.update(
                        {'_id': lotteryTime['_id']},
                        {'$set': {'exist': 0}})
                    break
                else:
                    client.send('0')

if __name__ == '__main__':
    server = LotterySever()
    server.start()
