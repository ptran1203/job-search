# CRAWL DATA FROM https://topitworks.com/vi/viec-lam

import scrapy
import requests
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from random import randrange
import asyncio
import json
import time
import requests

# constants
user_agents = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
]
disallow_path = ['/skill/', '/cong-ty/', '/city/']
job_url = []
max_deep = 3
crawled = []
host_url = "http://localhost:8000/api/store"

def bsfind(soup, tag, classes):
    res = soup.find(tag, classes)
    if res:
        return res.text.strip()
    return ''

def get_post_date(str):
    pos = str.lower().find('đã')
    return str[pos:].replace('  ', '').replace('\n', '')

def extract_url(item):
    atag = item.find('a')
    if atag:
        return atag.get('href')
    return '#'

def extract_img(item):
    img = item.find('img')
    if img:
        return img.get('src')
    return 'https://aliceasmartialarts.com/wp-content/uploads/2017/04/default-image.jpg'


def rand_headers():
    return {
        'User-Agent': user_agents[randrange(len(user_agents))]
    }

def is_accept_url(url):
    return '/viec-lam/' in url and not \
        any(_ in url for _ in disallow_path)


async def handle(url, deep=0):
    """
    Parse detail recursive
    """
    time.sleep(2)
    if (deep >= max_deep):
        return

    r =  requests.get(url, headers=rand_headers())
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')

    #find all anchor tags
    atag = soup.find_all('a', href=True)
    for tag in atag:
        url = tag['href']
        url not in crawled and handle(url, deep+1)

    item = soup.find('div', ['job-detail-data-wrapper'])
    if not item: return {}

    title = bsfind(item, 'h3', ['job-name'])
    salary_range = bsfind(item, 'strong', ['hidden-xs'])
    address = bsfind(item, 'p', ['company-location']).replace('  ', '').replace('\n', '')
    post_date = get_post_date(bsfind(item, 'span', ['job-post-day']))
    content = soup.find_all('div', ['read-more-content'])
    if content:
        content = "\n\n".join([_.text.strip() or '' for _ in content])
    # print(_.attrs['class'] for _ in content)
    data = {
        'post_url': url,
        'post_img': extract_img(item),
        'title': title,
        'content': content,
        'salary_range': salary_range,
        'post_date': post_date,
        'address': address
    }

    requests.post(host_url, json=data)
    crawled.append(url)

class Spider(scrapy.Spider):
    name = "example"
    google_cache_url = 'http://webcache.googleusercontent.com/search?q=cache:http://'
    allowed_domains = ['topitworks.com, webcache.googleusercontent.com']
    start_urls = (
        google_cache_url + 'topitworks.com/vi/viec-lam',
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            })

    def parse(self, response):
        """
        Parse url in page
        """
        for url in response.xpath('//a/@href').extract():
            if is_accept_url(url):
                job_url.append(url)


async def start():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(Spider)
    process.start()

    for url in job_url:
        url not in crawled and await handle(url)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
