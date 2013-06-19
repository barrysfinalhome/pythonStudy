#coding=utf-8
import pymongo
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
db = pymongo.MongoClient('mongodb://jianshi:jianshi@222.73.166.220:27017').YYPei
print "connected"
items = db.item.find({"seasons":  0, "editor.verified_date": {"$exists": "true"}})
print "fetched data"
print "total:", items.count()
file_out = codecs.open(u"/home/user/Desktop/items.txt", "w", "utf-8")
print "file opened"
print >>file_out, "seasons 0 items:"
for item in items:
    print >>file_out, u"_id: %s, title: %s" % (item["_id"], item["title"])
print >>file_out, "total:", items.count()
file_out.close()
