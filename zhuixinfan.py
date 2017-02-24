'''
collectors
'''
import re
from urllib.parse import quote
import operator
import functools
import requests
from collections import defaultdict
from bs4 import BeautifulSoup

RESOLUTION_RE = re.compile(r'\d{3,}X\d{3,}', re.I)
NO_RE = re.compile(r'\d{2,}')
ZHUIXINFAN_HOST = 'http://zhuixinfan.com/'


def zhuixinfan_collect(url):
    '''
        zhuixinfan collect
    '''
    r = requests.get(url)
    if not r.ok:
        return False
    bs = BeautifulSoup(r.content, 'html.parser')
    episodes = []
    for episode_tr in bs.select('.top-list-data tr')[1:]: # 排除列头
        tds = episode_tr.select('td')
        episode = {
            'title': tds[1].select('a')[0].contents[0],
            'url': ZHUIXINFAN_HOST + tds[1].select('a')[0].attrs['href'],
            'size': tds[2].contents[0],
        }
        episode['resolution'] = RESOLUTION_RE.findall(episode['title'])[0]
        episode['NO'] = NO_RE.findall(episode['title'])[0]
        episodes.append(episode)
    return episodes

def get_magnets(episodes):
    '''
        get magnet
    '''
    for episode in episodes:
        r = requests.get(episode['url'])
        episode['magnet'] = ''
        if r.ok:
            bs = BeautifulSoup(r.content, 'html.parser')
            episode['magnet'] = bs.select('#torrent_url')[0].contents[0]

    return episodes

if __name__ == '__main__':
    target_url = 'http://zhuixinfan.com/main.php?mod=viewresource&sid=8236'
    episodes_group_by_resolution = defaultdict(list)
    for episode in zhuixinfan_collect(target_url):
        resolution = functools.reduce(operator.mul, map(int, episode['resolution'].lower().split('x')))
        episodes_group_by_resolution[resolution].append(episode)
    episodes = sorted(episodes_group_by_resolution[max(episodes_group_by_resolution.keys())], key=lambda x:x['NO'])
    episodes = get_magnets(episodes)
    [print(_['magnet']) for _ in episodes]
