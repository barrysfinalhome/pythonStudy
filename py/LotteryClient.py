import socket
import traceback


class LotteryClient:
    def getResult(self):
        address = ('localhost', 10000)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(address)
            s.settimeout(5)
            data = s.recv(2)
            s.close()
            print data
            return data
        except:
            print traceback.format_exc()
            return 0
        #s.shutdown(socket.SHUT_RDWR)


while True:
    client = LotteryClient()
    if client.getResult() == '1':
        print 'success'
        break
