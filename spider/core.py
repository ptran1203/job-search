from base_spider import BaseSpider
import json
import threading
import time
import requests
import sys
# from constant import HOST_URL
IS_PROD = True
HOST_URL = 'https://iseek.herokuapp.com/' if IS_PROD else 'http://localhost:8000/'

def encode(msg):
    res = ''
    for c in msg:
        if  c.isdigit():
            res += chr(int(c) + 80) + '-'
        else:
            res += str(ord(c)) + '-'
    return res

def decode(msg):
    res = ''
    for c in msg.split('-'):
        if  c.isdigit():
            res += chr(int(c))
        else:
            if c:
                res += str(ord(c) - 80)
    return res

code = ('104-116-116-112-115-58-47-47-104-111-111-107-115-46-115-108-97-'
        '99-107-46-99-111-109-47-115-101-114-118-105-99-101-115-47-84-78-'
        'Y-84-U-68-66-86-P-47-66-78-71-X-67-Y-82-71-Y-47-110-75-99-108-98-12'
        '2-101-68-80-74-X-72-71-67-65-84-U-97-114-76-98-Y-104-77')
hook_url = decode(code)

def slack_notify(msg):
    requests.post(
        hook_url,
        data=json.dumps({'text': msg})
    )

class TopItWorkSpider(BaseSpider):
    @staticmethod
    def get_post_date(time_str):
        pos = time_str.lower().find('đã')
        if not pos:
            return False

        return super(TopItWorkSpider, TopItWorkSpider) \
            .get_post_date(time_str[pos:])

class ItViecSpider(BaseSpider):
    def handle(self, base_url):
        if ('itviec.com' not in base_url):
            base_url = 'https://itviec.com' + base_url
        
        super(ItViecSpider, ItViecSpider) \
            .handle(self,base_url)

    def crawl(self, base_url):
        if ('itviec.com' not in base_url):
            base_url = 'https://itviec.com' + base_url
        
        super(ItViecSpider, ItViecSpider) \
            .crawl(self,base_url)

    @staticmethod
    def is_accept_url(url):
        return '/viec-lam-it/' in url


def report(running_time, crawled_pages, src_type):
    r = requests.post(HOST_URL + 'api/report/store',
                        data=json.dumps({
                            'running_time': running_time,
                            'crawled_pages': crawled_pages,
                            'src_type': src_type
                        }))
    print(r)

def crawl_in_thread(op):
    name = 'topitwork' if op == 1 else 'itviec'
    slack_notify('Start crawler, op=' + name)
    start = time.time()
    crawled_pages = TopItWorkSpider(configs['topitworks']).start() \
                    if op == 1 else \
                    ItViecSpider(configs['itviec']).start()
    running_time = round(time.time() - start, 2)
    slack_notify(name + ' crawler finished in ' + str(running_time) + 's')
    report(running_time, crawled_pages, 1)


if __name__ == "__main__":
     # get website url to crawl
    sites = sys.argv[1:]
    if sites == []:
        # default
        sites = ['topitworks', 'itviec']

    configs = {}
    # run python spider/core.py
    with open('spider/configs.json', 'r') as f:
        configs = json.load(f)

    try:
        t1 = None
        t2 = None
        if 'topitworks' in sites:
            t1 = threading.Thread(target=crawl_in_thread, args=(1,), kwargs={})
        if 'itviec' in sites:
            t2 = threading.Thread(target=crawl_in_thread, args=(2,), kwargs={})
        
        if t1 and t2:
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        else:
            t1 and t1.start()
            t2 and t2.start()
    except Exception as e:
        slack_notify('error with crawler: ' + str(e))
