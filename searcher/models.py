from django.db import models
from helper import core as utils

class Searcher:
    def __init__(self, docs, vocab):
        self.docs = docs
        self.vocab = vocab

    def init_vector(self, q):
        terms = utils.norm_text(q).split(" ")
        vector = [0] * len(self.vocab)
        print(self.vocab)
        for term in terms:
            try:
                 vector[self.vocab.index(term)] += 1
            except ValueError:
                print("can not response query: ", term)

       
        return vector

    def search(self, q):
        res = {}
        qvector = self.init_vector(q)
        for doc in self.docs:
            res[doc.id] = utils.cosine(doc.get_vector(), qvector)

        print(res)

