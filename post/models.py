from django.db import models
from django.conf import settings
from django.utils import timezone
from bs4 import BeautifulSoup as bs
from requests import get
from datetime import datetime
from estimator import nn

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    salary_range = models.CharField(max_length=50)
    salary_estimated = models.FloatField(default=0)
    post_img = models.CharField(max_length=255)
    post_url = models.CharField(max_length=255)
    post_date = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=150, default='empty')
    create_date = models.DateTimeField(default=timezone.now)

    # use for vector space model
    vector = models.TextField(default='')
    fixed_vector = models.TextField(default='')

    def __str__(self):
        return self.title[:50]

    @classmethod
    def create(cls, obj):
        """
        Create new post and save
        """
        # prevent duplicate
        if cls.objects.filter(post_url=obj['post_url']).exists():
            return
        # convert time
        post_date = timezone.make_aware(
            datetime.strptime(obj['post_date'], "%m/%d/%Y - %H:%M:%S"))

        new = cls(
            title = obj['title'][:255],
            content = obj['content'],
            post_img = obj['post_img'][:255],
            post_url = obj['post_url'][:255],
            salary_range = obj['salary_range'],
            post_date = post_date,
            address = obj['address'][:150]
        )
        new.save()
        return new

    def get_date(self):
        return self.create_date.date()

    def get_text(self):
        return self.title + self.content

    def set_vector(self, vector):
        """
        set vector and save it
        """
        self.vector = ','.join([str(_) for _ in vector])
        self.save()

    def get_vector(self):
        try:
            return [float(_) for _ in self.vector.split(',')]
        except:
            return []

    def json_object(self, except_fields=[]):
        keys = ['id','title','content','post_img',
                'salary_range','post_url','post_date','address']
        return {k: getattr(self, k) for k in keys if k not in except_fields}

    def estimate_salary(self):
        self.salary_estimated = nn.predict(self.fixed_vector)

