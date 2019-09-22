
import scrapy
import requests
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool 
from random import randrange
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
disallow_path = ['/skill/', '/cong-ty/', '/city/', '/signin/']
skills = ['python','c++', 'asp', 'html', 'java',
    'javascript', 'ruby', 'nodejs', 'android',
    'ios', 'mysql', 'c++', 'php',]

job_url = []
max_deep = 3
crawled = []
host_url = "http://localhost:8000/api/store"
google_cache_url = 'http://webcache.googleusercontent.com/search?q=cache:http://'

def urls():
    topitworks_url = 'topitworks.com/vi/viec-lam'
    urls = [topitworks_url + '/skill/' + \
        skill for skill in skills] + [topitworks_url]
    return [google_cache_url + url for url in urls]

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
    return '/vi/viec-lam/' in url and not \
        any(_ in url for _ in disallow_path) and \
        url.count('/') == 5


def handle(url):
    """
    Parse detail recursive
    """
    # time.sleep(2)
    
    r =  requests.get(url, headers=rand_headers())
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')

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
    # print(data)
    # return
    requests.post(host_url, json=data)
    crawled.append(url)

def crawl(in_url):
    print('crawling ', in_url)
    r =  requests.get(in_url, headers=rand_headers())
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')

    #find all anchor tags
    atag = soup.find_all('a', href=True)
    i =0
    for tag in atag:
        url = tag['href']
        if (is_accept_url(url) and url not in crawled):
            handle(url)
            print('process: ', url)
    
    print('DONE----\n')



def start():
    for url in urls():
        crawl(url)


if __name__ == '__main__':
    start()