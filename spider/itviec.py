import scrapy
import requests
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from random import randrange
import asyncio
import json
import time
import requests

user_agents = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
]
disallow_path = ['/blog/', '/cong-ty/', '/city/']
job_url = []
max_deep = 3
crawled = []
host_url = "http://localhost:8000/api/store"


def absolute_url(url):
    return url if 'http' in url else 'http://itviec.com' + url

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

def is_accept_url(url):
    return '/viec-lam-it/' in url and not \
        any(_ in url for _ in disallow_path)

def rand_headers():
    return {
        'User-Agent': user_agents[randrange(len(user_agents))]
    }

def bsfind(soup, tag, classes):
    return (soup.find(tag, classes) or {}).text or ''

async def handle(url, deep=0):
        """
        Parse detail
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

        item = soup.find('div', ['job-detail'])
        if not item: return {}

        title = bsfind(item, 'h1', ['job_title'])
        salary_range = bsfind(item, 'div', ['salary']).strip()
        address = bsfind(item, 'div', ['address'])
        post_date = bsfind(item, 'div', ['distance-time-job-posted'])
        content = soup.find_all('div', ['job_description', 'skills_experience', 'love_working_here'])
        if content:
            content = "\n\n".join([_.text.strip() or '' for _ in content])
        data = {
            'post_url': url,
            'post_img': extract_img(item),
            'title': title,
            'content': content,
            'salary_range': salary_range,
            'address': address,
            'post_date': post_date
        }

        requests.post(host_url, json=data)
        crawled.append(url)

class Spider(scrapy.Spider):
    name = "example"
    google_cache_url = 'http://webcache.googleusercontent.com/search?q=cache:http://'
    allowed_domains = ['itviec.com, webcache.googleusercontent.com']
    start_urls = (
        google_cache_url + 'itviec.com/viec-lam-it',
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
        disallow_path = ['/skill/', '/cong-ty/', '/city/']
        for l in response.xpath('//a/@href').extract():
            # job_url.append(l)
            if '/viec-lam-it/' in l and not any(_ in l for _ in disallow_path):
                job_url.append(l)



async def start():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(Spider)
    process.start()
    import json
    import time
    import requests
    

    for url in job_url:
        url not in crawled and await handle(absolute_url(url))
        time.sleep(2)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())