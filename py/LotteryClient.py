import socket
import traceback
import time


class LotteryClient:
    def getResult(self):
        address = ('localhost', 10000)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
        s.settimeout(5)
        data = s.recv(2)
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        print data
        return data
       
        #s.shutdown(socket.SHUT_RDWR)

if __name__ == '__main__':
    while True:
        client = LotteryClient()
        if client.getResult() == '1':
            print 'success'            
