import scrapy
import requests
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from random import randrange
# from .models import Post

# https://stackoverflow.com/questions/30345623/scraping-dynamic-content-using-python-scrapy
# http://webcache.googleusercontent.com/search?q=cache:http://topitworks.com/vi/viec-lam
user_agents = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
]

job_url = []

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

def parse(url):
        """
        Parse detail
        """
        r =  requests.get(url, headers=rand_headers())
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        item = soup.find('div', ['job-detail-data-wrapper'])

        if not item: return {}

        title = item.find('h3', ['job-name'])
        if title:
            title = title.text or ''

        content = soup.find_all('div', ['read-more-content'])
        # print(_.attrs['class'] for _ in content)
        if content:
            content = "\n\n".join([_.text.strip() or '' for _ in content])

        salary_range = item.find('strong', ['hidden-xs'])

        if salary_range:
            salary_range = (salary_range.text or '').strip()
        return {
            'post_url': url,
            'post_img': extract_img(item),
            'title': title,
            'content': content,
            'salary_range': salary_range
        }

        # return data or {}

class Spider(scrapy.Spider):
    name = "example"
    google_cache_url = 'http://webcache.googleusercontent.com/search?q=cache:http://'
    allowed_domains = ['topitworks.com, webcache.googleusercontent.com']
    start_urls = (
        google_cache_url + 'topitworks.com/vi/viec-lam',
        # 'http://topitworks.com/vi/viec-lam'
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
            if '/viec-lam/' in l and not any(_ in l for _ in disallow_path):
                job_url.append(l)


def start():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(Spider)
    process.start()
    import json
    import time

    with open('save.json', 'w') as f:
        for url in job_url:
            data = parse(url)
            json.dump(data, f)
            time.sleep(5)

if __name__ == '__main__':
    start()