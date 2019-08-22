from django.db import models
from django.conf import settings
from django.utils import timezone
from bs4 import BeautifulSoup as bs
from requests import get

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


# helper
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

def create_soup(url):
    response = get(url, headers=headers)
    return bs(response.text, 'html.parser')

# Create your models here.
class BaseCrawler(models.Model):
    # crawl_url = ''
    # DB fields
    title = models.CharField(max_length=255)
    content = models.TextField()
    post_img = models.CharField(max_length=255)
    post_url = models.CharField(max_length=255)
    create_date = models.DateTimeField(default=timezone.now)

    @classmethod
    def create(cls, obj):
        # print(obj)
        print(obj['title'])
        new = cls(
            title = obj['title'][:255],
            content = obj['content'],
            post_img = obj['post_img'][:255],
            post_url = obj['post_url'][:255],
        )
        print("DONENEEE")
        new.save()
        return new

    def get_date(self):
        return self.create_date.date()

class TechTalk(BaseCrawler):

    def __init__(self):
        self.data = self.crawl()
    @staticmethod
    def crawl():
        """
        Crawl data
        """
        url = 'https://techtalk.vn/resources'
        soup = create_soup(url)
        items = soup.find_all('div', ['td-block-span4'])
        data = []
        for item in items:
            title = item.find('h3', ['entry-title'])
            if title:
                title = title.text or ''
            content = item.find('div', ['td-excerpt'])
            if content:
                content = content.text or ''
            data.append({
                'post_url': extract_url(item),
                'post_img': extract_img(item),
                'title': title,
                'content': content
            })
        
        return data or {}

    def save(self):
        for d in self.data:
            super().create(d)


