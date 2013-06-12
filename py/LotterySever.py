#FileName : LotteryServer
import socket
import pymongo
import time


class LotterySever:
    '''Lottery Class'''
    lotteryTime = None
    exist = True

    def __init__(self, dbhost='localhost', port=27017):
        db = pymongo.MongoClient(dbhost, port).test
        self.lotteryTime = db.lottery.find()

    def start(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", 10000))
        server.listen(10)
        print "server is open on 10000"
        while True:
            client, addr = server.accept()
            time.sleep(2)
            if time.time() >= self.lotteryTime and self.exist is True:
                client.send('1')
                self.exist = False
            else:
                client.send('0')
            client.close()

if __name__ == '__main__':
    server = LotterySever()
    server.start()
