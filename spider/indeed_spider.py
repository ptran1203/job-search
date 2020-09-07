import requests
import os
from bs4 import BeautifulSoup
import json
import datetime
import time

headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

class IndeedSpider:
    def __init__(self):
        self.base_url = 'https://vn.indeed.com'
        self.keywords = [
                         'data scientist', 'machine learning',
                         'computer vision', 'back-end', 'front-end',
                         'dev-ops',
                        ]
        self.locations = ['Thành phố Hồ Chí Minh', 'Hà Nội']
        self.crawled = []


    def query_string(self, keyword, location, start):
        return '?q={}&l={}&start={}'.format(keyword, location, start)


    @staticmethod
    def _get(url):
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        return r


    def start(self):
        for l in self.locations:
            for q in self.keywords:
                for p in [0, 10, 20, 30, 40]:
                    self.crawl(self.base_url + '/jobs' + self.query_string(q,l,p))


    def is_accept_url(self, url):
        return 'viewjob' in url or '/rc' in url
    
    def crawl(self, url):
        try:
            r = self._get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            atag = soup.find_all('a', href=True)
            for tag in atag:
                url = tag['href']
                if 'http' not in url:
                    url = self.base_url + url
                if (self.is_accept_url(url) and url not in self.crawled):
                    self.handle(url)
        except Exception as e:
            print(str(e))

    
    @staticmethod
    def bsfind(soup, tag, classes):
        res = soup.find(tag, classes)
        if res:
            return res.get_text('\n', True)
        return ''


    def handle(self, url):
        global html
        time.sleep(2)
        print("Scraping {} ...".format(url))

        r = self._get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        item = soup.find('div', 'jobsearch-ViewJobLayout-jobDisplay')
        if not item:
            return {}

        salary = self.bsfind(item, 'span', 'icl-u-xs-mr--xs')
        address = self.bsfind(item, 'div', 'jobsearch-InlineCompanyRating')
        title = self.bsfind(item, 'h1', 'jobsearch-JobInfoHeader-title')
        content = self.bsfind(item, 'div', 'jobsearch-jobDescriptionText')
        post_date = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")

        stt = requests.post('http://iseek.herokuapp.com' + '/api/store', data=json.dumps({
            'post_url': url,
            'post_date': post_date,
            'content': content,
            'title': title,
            'address': address,
            'salary_range': salary,
            'post_img': 'none',
        }))
        print("Insert ", stt)

        self.crawled.append(url)
        print(self.crawled)
