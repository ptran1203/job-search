from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool 
from random import randrange
import json
import time
import datetime
import requests
import re


# -------------------- constants --------------------
crawled = []
disallow_path = ['/skill/', '/cong-ty/', '/city/', '/signin/']
extend_path = ['/skill/', '/cong-ty/', '/city/',
'python','c++', 'asp', 'html', 'java',
    'javascript', 'ruby', 'nodejs', 'android',
    'ios', 'mysql', 'c++', 'php', 
    '-jd' #vietnamwork
    ]
max_deep = 7
# host_url = 'http://localhost:8000' 
host_url = 'http://iseek.herokuapp.com'
digit_regex = re.compile(r'\d+')

# -------------------- classes --------------------
class BaseSpider:
    """
    Base spider, can crawl common job site
    topitworks, itviec, ...
    """

    def __init__(self, init_data):
        """
        schema in configs.json
        """
        self.selector = {
            'tag': init_data['tag'],
            'classes': init_data['classes']
        }
        self.base_url = init_data['base_url']
        self.count_extend = 0
        self.counter = 0

    @staticmethod
    def is_accept_url(url):
        return '/vi/viec-lam/' in url and not \
            any(_ in url for _ in disallow_path) and \
            url.count('/') == 5

    @staticmethod
    def rand_headers():
        return {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}


    @staticmethod
    def extract_img(item):
        return ""


    @staticmethod
    def bsfind(soup, tag, classes):
        res = soup.find(tag, classes)
        if res:
            return res.get_text('\n', True)
        return ''

    @staticmethod
    def get_post_date(date_str):
        date_str = date_str.lower()
        # find digit value
        match = digit_regex.search(date_str)
        time = None
        now = datetime.datetime.now()
        if match:
            time = int(match.group())
            # <time> days ago
            if 'ngày' in date_str:
                # save job at least 15 days ago
                if time > 15:
                    return False
                return (now - datetime.timedelta(days=time)) \
                    .strftime("%m/%d/%Y - %H:%M:%S")
            elif 'giờ' in date_str:
                return (now - datetime.timedelta(hours=time)) \
                    .strftime("%m/%d/%Y - %H:%M:%S")
            elif 'phút' in date_str:
                return (now - datetime.timedelta(minutes=time)) \
                    .strftime("%m/%d/%Y - %H:%M:%S")
            # do not save expired job
            elif 'tháng' in date_str:
                return False


        return False

    @staticmethod
    def extract_url(item):
        atag = item.find('a')
        if atag:
            return atag.get('href')
        return '#'

    def handle(self, base_url):
        """
        Parse detail recursive
        """
        time.sleep(2)
        print('handling', base_url)

        r =  requests.get(base_url,
            headers=self.rand_headers())
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        item = soup.find(
            self.selector['tag']['base'],
            self.selector['classes']['base']
        )
        if not item: return {}
        post_date = self.parse_post_date(item)
        data = {
            'post_url': base_url,
            'post_img': self.extract_img(item),
            'title': self.parse_title(item),
            'content': self.parse_content(soup, item),
            'salary_range': self.filter_salary(self.parse_salary(item)),
            'post_date':post_date,
            'address': self.parse_address(item).replace('Xem bản đồ', '')
        }

        post_date and requests.post(host_url + '/api/store', json=data)
        self.done()

        # crawl deeper
        atag = soup.find_all('a', href=True)
        for tag in atag:
            _url = tag['href']
            if any(_ in _url for _ in extend_path) \
                and _url not in crawled:
                crawled.append(_url)
                self.crawl(_url)

    @staticmethod
    def filter_salary(salary):
        if '$' in salary:
            return salary
        return ''

    def parse_title(self, item):
        tag = self.selector['tag']['title']
        classes = self.selector['classes']['title']
        return self.bsfind(item, tag, classes)

    def parse_salary(self, item):
        tag = self.selector['tag']['salary']
        classes = self.selector['classes']['salary']
        return self.bsfind(item, tag, classes)

    def parse_address(self, item):
        tag = self.selector['tag']['address']
        classes = self.selector['classes']['address']
        return self.bsfind(
            item, tag, classes
            ).replace('  ', '').replace('\n', '')

    def parse_post_date(self, item):
        tag = self.selector['tag']['post_date']
        classes = self.selector['classes']['post_date']
        return self.get_post_date(
            self.bsfind(item, tag, classes)
        )

    def parse_content(self, soup, item):
        tag = self.selector['tag']['content']
        classes = self.selector['classes']['content']
        content = soup.find_all(tag, classes)
        if content:
            return "\n\n".join([_.get_text('\n', True) or '' for _ in content])
        return ''

    def done(self):
        """
        call when finnish crawl a page
        update counter
        """
        self.counter += 1

    def crawl(self, base_url):
        self.count_extend += 1
        if self.count_extend > max_deep:
            return
        try:
            r = requests.get(base_url, headers=self.rand_headers())
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')
            #find all anchor tags
            atag = soup.find_all('a', href=True)
            for tag in atag:
                url = tag['href']
                if (self.is_accept_url(url) and url not in crawled):
                    self.handle(url)
        except Exception as e:
            print(e)
            print('!Warning `invalid url`', base_url)

    def start(self):
        # return 564
        self.crawl(self.base_url)
        return self.counter
