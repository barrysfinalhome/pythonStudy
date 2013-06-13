#coding:utf-8
#FileName:LotteryTime
import time
import datetime
#import random
import pymongo
daySecond = 24*60*60  # 一天的秒
hourSecond = 60*60  # 一小时的秒
days = 1
timeStartBound = 20  # 起始时间
timeEndBound = 24
timeEndBound = timeEndBound - 0.1 * (timeEndBound - timeStartBound)  # 提前截至时间 预留足够时间产生大奖

nowDate = time.mktime(datetime.date.today().timetuple())
#create random time
#lotteryTime = nowDate + random.randint(timeStartBound * hourSecond, timeEndBound * hourSecond)
#create test time
lotteryTime = time.time() + 30
db = pymongo.MongoClient('localhost', 27017).test
while lotteryTime <= nowDate+daySecond:
    lotteryTime += 30
    db.lottery.insert({
        'level': 1,
        'timestamp': lotteryTime,
        'time': datetime.datetime.fromtimestamp(lotteryTime),
        'exist': '1'})
