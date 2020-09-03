from post.models import Post
from helper import processor
from django.db import models
import re
import math

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
        1 -> exist in vocabulary1
    """ 
    word = models.CharField(max_length=100)
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
            res[doc.id] = processor.cosine(doc.get_vector(), qvector)

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
        return str(self.size)

    def init_vocab_posts(self):
        """
        Initialize vocabulaty from posts
        """
        posts = Post.objects.all()
        vocab = set()
        for post in posts:
            [vocab.add(_) for _ in \
                processor.cleaned_text(post.get_text())]

        return list(vocab), posts

    @staticmethod
    def generate_inverted_index(vocab, posts):
        """
        {
            'python': [75: 2, 77: 3],
            'java': [18: 2, 5: 15, 489: 21]
            ...
        }
        """
        inverted_indexes = {term: {} for term in vocab}
        for post in posts:
            for word in processor.cleaned_text(post.get_text()):
                try:
                    key = inverted_indexes[word]
                    if post.id in key:
                        key[post.id] += 1
                    else:
                        key[post.id] = 1
                except Exception as e:
                    print(e)
        
        return inverted_indexes

    @staticmethod
    def _idfs(inverted_indexes, size):
        """
        calculate idf for each term in vocab
        return new list, position map 1:1 with vocab
        """
        result = {}
        for term, idx in inverted_indexes.items():
            result[term] = len(idx)
        # log base 2 of size/1 + count

        return {term: math.log(size / (1 + count), 2) \
                         for term, count in result.items()}

    @staticmethod
    def _tfidf(vector, idfs):
        """
        weigh of term is tf*idf
        return new vector
        """
        for i in range(vector):
            vector[i] = vector[i] * idfs[i]

        return vector

    def build(self, vocab, posts):
        """
        Start build vector for each post
        every element in vector is the product of tf, idf
        """
        inverted_indexes = self.generate_inverted_index(vocab, posts)
        idf_map = self._idfs(inverted_indexes, len(vocab))

        # set tf in vector
        post_map = {p.id:[0]*len(vocab) for p in posts}
        for term, post_count in inverted_indexes.items():
            for post_id, count in post_count.items():
                tf = 1 + math.log(count) if count > 0 else 0
                post_map[post_id][vocab.index(term)] = \
                        round(tf * idf_map[term], 2)

        for post in posts:
            post.set_vector(post_map[post.id])

        Vocabulary.objects.all().delete()
        Vocabulary.objects.create(data=','.join(vocab),
                                    count=len(vocab))
        return len(post_map)
