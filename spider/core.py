from base_spider import BaseSpider
import json
import threading
import time
import requests
import sys
# from constant import HOST_URL
IS_PROD = True
HOST_URL = 'https://iseek.herokuapp.com/' if IS_PROD else 'http://localhost:8000/'


def slack_notify(msg):
    requests.post(
        'https://hooks.slack.com/services/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',
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
        if 'topitworks' in sites:
            start = time.time()
            crawled_pages = TopItWorkSpider(configs['topitworks']).start()
            running_time = round(time.time() - start, 2)
            slack_notify('topitwork crawler finished in ' + str(running_time) + 's')
            # report(running_time, crawled_pages, 1)
        if 'itviec' in sites:
            start = time.time()
            crawled_pages = ItViecSpider(configs['itviec']).start()
            running_time = round(time.time() - start, 2)
            slack_notify('itviec crawler finished in ' + str(running_time) + 's')
            # report(running_time, crawled_pages, 2)
    except Exception as e:
        slack_notify('error with crawler: ' + str(e))
