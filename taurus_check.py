# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
import pymongo

this_month = [1,2,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
next_month = [1,2,6,7,10,11,14]

class Checker(object):
    """docstring for Checker"""
    def __init__(self, dates):
        super(Checker, self).__init__()
        self.db = pymongo.MongoClient()
        self.dates = dates
        self.today = datetime(*datetime.now().timetuple()[:3])

    def check_taurus(self):
        if self.today.day not in self.dates:
            [self.check_taurus_candid_raw(self.today + timedelta(x)) for x in xrange(3)]
        else:
            day = self.today
            while day.day in self.dates:
                self.check_taurus_candid_raw(day)
                day += timedelta(1)

    def check_taurus_candid_raw(self, day):
        print day
        return 1

    def check_weather(self):
        pass

if __name__ == '__main__':
    dataChecker = Checker(this_month)
    dataChecker.check_taurus()
    dataChecker.check_weather()
