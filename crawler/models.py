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
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    post_img = models.CharField(max_length=255)
    post_url = models.CharField(max_length=255)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title[:50]

    @classmethod
    def create(cls, obj):
        """
        Create new post and save
        """
        new = cls(
            title = obj['title'][:255],
            content = obj['content'],
            post_img = obj['post_img'][:255],
            post_url = obj['post_url'][:255],
        )
        new.save()
        return new

    def get_date(self):
        return self.create_date.date()