import re
import math
import requests
'''
'''

RE_PEOPLE_NAME = re.compile(r'href=\"\/people\/(?P<name>[^("/)]*)"')
HOST = 'https://www.zhihu.com/'

JAR = requests.cookies.RequestsCookieJar()
JAR.set('login', '"MjQzZTM5YjQwMTliNGIyYjhlMWRlMmNkY2EzNTEwMWQ=|1485532035|48d1bf2e033d512f0798fecc1fa5d729fb8e43db"', domain='.zhihu.com', path='/')

ANSERVER_ID = '21488267'
# ANSERVER_ID = '29801420'
OUT_FILE = open('./%s.txt' % ANSERVER_ID, 'w')

r = requests.get(HOST + 'answer/%s/voters_profile?offset=0' % ANSERVER_ID, headers={
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }, cookies=JAR).json()
TOTAL = r.get('paging', {}).get('total')
MISS_COUNT = 0
def get_names(url):
    global MISS_COUNT
    result = []
    r = requests.get(url, headers={
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }, cookies=JAR).json()
    for people_html in r.get('payload'):
        people_name = RE_PEOPLE_NAME.findall(people_html)
        print(people_name)
        if not people_name:
            MISS_COUNT += 1
        else:
            result.append(people_name)
            OUT_FILE.write(people_name[0] + '\n')
    # next_page = r.get('paging', {}).get('next')
    # if next_page:
    #     result.extend(get_names(HOST + next_page))
    return result

for i in range(math.ceil(TOTAL/10)):
    result = []
    url = HOST + ('/answer/%s/voters_profile?offset=%s' % (ANSERVER_ID, i*10))
    print(url)
    result.extend(get_names(url))
    OUT_FILE.flush()

print(result)
