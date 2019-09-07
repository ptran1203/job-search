from post.models import Post
from helper.common import norm_text
from django.db import models
from helper import common as commonHelper
import re

# build vector space model
class Vocabulary(models.Model):
    data = models.TextField()

    def get(self):
        return self.data.split(',')
    
    def __str__(self):
        return 'data'


class VectorSpace:
    def __init__(self):
        """
        Create vsmodel
        """
        vocab, posts = self.init_vocab_posts()
        self.size = self.build(vocab, posts)
    
    def __str__(self):
        return self.size

    def init_vocab_posts(self):
        """
        Initialize vocabulaty from posts
        """
        posts = Post.objects.all()
        vocab = set()
        for post in posts:
            [vocab.add(_) for _ in \
                commonHelper.cleaned_text(post.get_text())]

        return list(vocab), posts

    def build(self, vocab, posts):
        """
        Start build vector for each post
        return number of posts
        """
        post_map = {p.id:[0]*len(vocab) for p in posts}
        for post in posts:
            for word in commonHelper.cleaned_text(post.get_text()):
                try:
                    post_map[post.id][vocab.index(word)] += 1
                except KeyError:
                    print("WARNING: ", post.id, "not in map")

        for post in posts:
            post.set_vector(post_map[post.id])

        Vocabulary.objects.all().delete()
        Vocabulary.objects.create(data=','.join(vocab))
        return len(post_map)
