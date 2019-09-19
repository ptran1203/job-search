from django.db import models
from django.conf import settings
from django.utils import timezone
from bs4 import BeautifulSoup as bs
from requests import get
from helper import common as commonHelper

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    salary_range = models.CharField(max_length=50)
    post_img = models.CharField(max_length=255)
    post_url = models.CharField(max_length=255)
    create_date = models.DateTimeField(default=timezone.now)

    # use for vector space model
    vector = models.TextField(default='')

    def __str__(self):
        return self.title[:50]

    @classmethod
    def create(cls, obj):
        """
        Create new post and save
        """
        # prevent duplicate
        if cls.objects.filter(title = obj['title'][:255]).exists():
            return
        new = cls(
            title = obj['title'][:255],
            content = obj['content'],
            post_img = obj['post_img'][:255],
            post_url = obj['post_url'][:255],
            salary_range = obj['salary_range'],
        )
        new.save()
        return new

    def get_date(self):
        return self.create_date.date()

    def get_text(self):
        return self.title + self.content + self.salary_range

    def set_vector(self, vector):
        """
        set vector and save it
        """
        self.vector = ','.join([str(_) for _ in vector])
        self.save()
    
    def get_vector(self):
        return [int(_) for _ in self.vector.split(',')]

    def json_object(self, **kwargs):
        content = self.content if \
                not kwargs['is_html'] else \
                commonHelper.split_content(self.content)
        return {
            'id': self.pk,
            'title': self.title,
            'content': content,
            'post_img': self.post_img,
            'salary_range': self.salary_range,
            'post_url': self.post_url
        }