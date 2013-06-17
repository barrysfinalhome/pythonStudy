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
                 '$lte': time.time() + 24*60*60
                 },
             'exist': '1'
             },
            sort=[('time', 1)])

    #start server
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", 10000))
        server.listen(10)  # set the max number of connctions
        print "server is open on 10000"
        for lottery_time in self.lotteryTimes:
            print lottery_time
            while True:
                client, addr = server.accept()
                if time.time() >= lottery_time['timestamp']:
                    this_id = lottery_time['_id']
                    if self.db.lottery.find(
                        {'_id': this_id,
                         'exist': 1
                         }):    # check if the award is exist
                        self.db.lottery.update(
                            {'_id': this_id},
                            {'$inc': {'exist': -1}})
                        if self.db.lottery.find(
                                {'_id': this_id,
                                 'exist': 1
                                 }):
                            client.send('0')
                        client.send('1')
                    break
                else:
                    client.send('0')

if __name__ == '__main__':
    server = LotterySever()
    server.start()
