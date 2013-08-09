# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from datetime import timedelta

import Momo.base.mongo as mongo

calendar = {8: [10, 11, 17, 18, 24, 25, 31],
            9: [1, 7, 8, 14, 15, 21, 22, 28, 29]}

DRESS_TYPE = ['PROFESSIONAL', 'LEISURE', 'FASHION', 'SELFHOOD', 'COMMUTE']

class Checker(object):
    """docstring for Checker"""
    def __init__(self, dates):
        super(Checker, self).__init__()
        self.mongo_db = mongo.get_mongo()
        self.candid_raw_col = self.mongo_db.db[mongo.CollectionNames.TAURUS_CANDID_RAW]
        self.candid_col = self.mongo_db.db[mongo.CollectionNames.TAURUS_CANDID]
        self.dates = dates
        self.today = datetime(*datetime.now().timetuple()[:3])
        self.city_codes = self.mongo_db.db[mongo.CollectionNames.MANUAL_DATA].\
            find_one({'_id': 'cities'})['value']

    def check_taurus(self):
        if self.today.day not in self.dates[self.today.month]:
            [self.check_taurus_candid_raw_valid(self.today + timedelta(x)) for x in xrange(3)]
        else:
            day = self.today
            i = 0
            while True:
                invalid_types = [DRESS_TYPE[x] for x in self.check_taurus_candid_raw_valid(day)]
                if not len(invalid_types):
                    print 'the type %s in %s is invalid' % (invalid_types, day)
                    if i < 2:
                        logging.error('the type %s in %s is invalid' % (invalid_types, day))
                    else:
                        logging.warn('the type %s in %s is invalid' % (invalid_types, day))
                if day.day not in self.dates[day.month]:
                    break
                i += 1
                day = self.today + timedelta(i)
    def check_taurus_candid_raw_valid(self, day):
        invalid_types = []
        for candid_type in xrange(5):
            candid_raw = self.candid_raw_col.find_one({'target_date':day, 'type': candid_type})
            if not (candid_raw and candid_raw.get('brief') and candid_raw.get('detail')
                and candid_raw.get('generatedPics') and candid_raw.get('items')):
                return invalid_types.append(candid_type)
        return invalid_types

    def check_weather(self):
        day = self.today
        for i in xrange(1):
            day = day + timedelta(1)
            str_day = day.strftime('%Y%m%d')
            for (key, value) in self.city_codes.items():
                for candid_type in xrange(5):
                    candid = self.candid_col.find_one({'_id': '%s_%s_%s' % (str_day, key, candid_type) })
                    if not (candid and candid.get('weather') and candid['weather'].get('weatherValue')
                        and candid['weather'].get('iconName') and candid['weather'].get('windStr')
                        and candid['weather'].get('tempStr')):
                        logging.error(u'%s（%s）城市在%s日穿衣类型为%s的数据无效' % (value['cname'], key,
                            str_day, DRESS_TYPE[candid_type]))
                    logging.info(u'%s（%s）城市在%s日穿衣类型为%s的数据OK' % (value['cname'], key,
                            str_day, DRESS_TYPE[candid_type]))

if __name__ == '__main__':
    dataChecker = Checker(calendar)
    dataChecker.check_taurus()
    dataChecker.check_weather()
