#filename comparescript
import re
str_src = "Content_type=json&apiPType=openapi&apiCategoryId=openapi.product&sip_apiname=Yintai.OpenApi.Item.GetChangeProductPricePageList_1.0&datasetting=test&sip_http_method=post&signtype=0&Language=Chinese&ClientName=%E7%B3%BB%E7%BB%9F%E5%88%86%E9%85%8D&ClientId=1010409&Timereq=20101102164257&Date=20130617193623&channelID=1010409&startTime=2013-01-01+00%3A00%3A00&endTime=2013-07-01+00%3A00%3A00&currentPage=0&method=Yintai.OpenApi.Item.GetChangeProductPricePageList&ver=1.0"
str_my = "Content_type=json&apiPType=openapi&apiCategoryId=openapi.product&sip_apiname=Yintai.OpenApi.Item.GetChangeProductPricePageList_1.0&datasetting=test&sip_http_method=post&Language=Chinese&ClientName=suge&ClientId=1010409&Timereq=20101102164257&Date=20130225201724&channelID=1010409&startTime=2013-06-17+07%3A31%3A19&endTime=2013-06-17+07%3A36%3A19&currentPage=0&method=Yintai.OpenApi.Item.GetChangeProductPricePageList&ver=1.0"
str_src_list = re.split("&|=", str_src)
str_my_list = re.split("&|=", str_my)
set_src = set()
set_my = set()

dict_src = {}
dict_my = {}
for i in range(len(str_src_list)/2):
    dict_src[str_src_list[2*i]] = str_src_list[2*i + 1]
    set_src.add(str_src_list[2*i])
    set_src.add(str_src_list[2*i + 1])

for i in range(len(str_my_list)/2):
    dict_my[str_my_list[2*i]] = str_my_list[2*i + 1]
    set_my.add(str_my_list[2*i])
    set_my.add(str_my_list[2*i + 1])

print set_src ^ set_my

for k in dict_src:
    if dict_src[k] in dict_my : print 
    if dict_src[k] != dict_my[k]:
        print "src[%s]" % k, dict_src[k], " ", "my[%s]" % k, dick_my[k]
