#coding=utf-8
import pymongo
import sys
import re
import codecs
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf-8')
mongo_db = pymongo.MongoClient('mongodb://jianshi:jianshi@222.73.166.220:27017')
#mongo_db = pymongo.MongoClient('mongodb://p2buser:p2bpass@192.168.1.102:27018')
crawlerdate = ['TB_CRAWL', 'TB_ITEM', 'tbi']
#crawlerdate = ['YT_CRAWL', 'YT_ITEM', 'yti']
#crawlerdate = ['ZARA_CRAWL', 'ZARA_ITEM', 'zai']
#crawlerdate = ['YM_CRAWL', 'YM_ITEM', 'ymi']
db = mongo_db[crawlerdate[0]]
print "connected"
tb_items = db[crawlerdate[1]].find({"state":  'delete'}, ['_id', 'partial_update_time'])
print "fetched data from " + crawlerdate[0]
print "total:", tb_items.count()

db = mongo_db.YYPei
rexExp = re.compile(crawlerdate[2], re.IGNORECASE)
items = db.item.find({'_id': rexExp}, ['_id'])
print "fetched data from YYPei"
print "total:", items.count()


dict_item = {}
for item in items:
    dict_item[item['_id']] = item

count = 0
counttime = 0
countselftime =0

file_out = codecs.open(u"/home/user/Desktop/err_items" + str(time.time()) + ".txt", "w", "utf-8")
file_out_ignorn = codecs.open(u"/home/user/Desktop/err_ignorn_items" + str(time.time()) + ".txt", "w", "utf-8")
dict_err_item = {}

for tb_item in tb_items:
    if tb_item.get('partial_update_time') > datetime.datetime(2013, 4, 14):
        countselftime += 1
    if dict_item.get('tbi' + str(tb_item['_id'])):
        count += 1
        if tb_item['_id'] == 22827024649 or tb_item['_id'] == 15224249838:
            print tb_item['partial_update_time']
        print >>file_out, u"_id: %s" % (tb_item["_id"])
        if tb_item.get('partial_update_time') > datetime.datetime(2013, 4, 14):
            print >>file_out_ignorn, u"_id: %s, time: %s" % (tb_item["_id"], tb_item['partial_update_time'])
            counttime += 1

print count
print counttime
print "tbku count: %s", countselftime
file_out.close()
file_out_ignorn.close()
