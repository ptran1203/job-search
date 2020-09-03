from base_spider import BaseSpider
from indeed_spider import IndeedSpider
import json
import threading
import time
import requests
import sys
# from constant import HOST_URL
IS_PROD = True
HOST_URL = 'https://iseek.herokuapp.com/' if IS_PROD else 'http://localhost:8000/'

class TopCvSpider(BaseSpider):
    @staticmethod
    def get_post_date(time_str):
        pos = time_str.lower().find('đã')
        if not pos:
            return False

        return super(TopCvSpider, TopCvSpider) \
            .get_post_date(time_str[pos:])

    @staticmethod
    def is_accept_url(url):
        return '/viec-lam/' in url

class ItViecSpider(BaseSpider):
    def handle(self, base_url):
        if 'itviec.com' not in base_url:
            base_url = 'https://itviec.com' + base_url
        
        super(ItViecSpider, ItViecSpider) \
            .handle(self,base_url)

    def crawl(self, base_url):
        if 'itviec.com' not in base_url:
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

def crawl_in_thread(op):
    start = time.time()
    if op == 1:
        crawled_pages = IndeedSpider().start()
    else:
        crawled_pages = ItViecSpider(configs['itviec']).start()

    running_time = round(time.time() - start, 2)
    report(running_time, crawled_pages, 1)


if __name__ == "__main__":
     # get website url to crawl
    sites = sys.argv[1:]
    if sites == []:
        # default
        sites = ['topcv', 'itviec1']

    configs = {}
    # run python spider/core.py
    with open('spider/configs.json', 'r') as f:
        configs = json.load(f)

    try:
        t1 = None
        t2 = None
        t1 = threading.Thread(target=crawl_in_thread, args=(1,), kwargs={})
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
        pass
