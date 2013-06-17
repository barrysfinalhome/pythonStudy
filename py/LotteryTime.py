#coding:utf-8
#FileName:LotteryTime
import time
import datetime
#import random
import pymongo
day_second = 24*60*60  # 一天的秒
hour_second = 60*60  # 一小时的秒
days = 1
time_star_bound = 20  # 起始时间
time_end_boudn = 24
time_end_boudn = time_end_boudn - 0.1 * (time_end_boudn - time_star_bound)  # 提前截至时间 预留足够时间产生大奖

now_date = time.mktime(datetime.date.today().timetuple())
#create random time
#lottery_time = now_date + random.randint(time_star_bound * hour_second, time_end_boudn * hour_second)
#create test time
lottery_time = time.time() + 30
db = pymongo.MongoClient('localhost', 27017).test
while lottery_time <= now_date+day_second:
    lottery_time += 30
    db.lottery.insert({
        'level': 1,
        'timestamp': lottery_time,
        'time': datetime.datetime.fromtimestamp(lottery_time),
        'exist': '1'})
