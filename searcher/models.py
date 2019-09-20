from post.models import Post
from helper.common import norm_text
from helper import common as commonHelper
from django.db import models
import re

# Django models
class Vocabulary(models.Model):
    data = models.TextField()
    count = models.IntegerField(default=0)

    def get(self):
        return self.data.split(',')
    
    def __str__(self):
        return str(self.count)

class Keywords(models.Model):
    """
    Store user search key words

    status_type:
        0 -> not exist in vocabulary
        1 -> exist in vocabulary
    """ 
    word = models.CharField(max_length=20)
    num_of_searches = models.IntegerField(default=0)
    status_type = models.IntegerField(default=0)

    def __str__(self):
        return self.word

    def json_object(self):
        return {
            'id': self.pk,
            'word': self.word,
            'num_of_searches': self.num_of_searches,
            'status_type': self.status_type
        }


class Searcher:
    def __init__(self, docs, vocab):
        self.docs = docs
        self.vocab = vocab

    def init_vector(self, terms):
        vector = [0] * len(self.vocab)
        for term in terms:
            try:
                 vector[self.vocab.index(term)] += 1
            except ValueError:
                print("can not response query: ", term)

        return vector

    def search(self, terms):
        res = {}
        qvector = self.init_vector(terms)
        # print([x for x in qvector if x != 0])
        for doc in self.docs:
            res[doc.id] = commonHelper.cosine(doc.get_vector(), qvector)

        doc_ids = sorted(res.items(), key=lambda kv: -kv[1])
        # print(doc_ids)
        return [doc[0] for doc in doc_ids if doc[1] > 0.0]

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
        Vocabulary.objects.create(data=','.join(vocab), count=len(vocab))
        return len(post_map)