import gensim.models
import numpy as np


class Embedding:
    def __init__(self):
        self.model = gensim.models.Word2Vec.load("models/storage/word2vec_model")

    def word2vec(self, word):
        if word in self.model.wv.vocab:
            return self.model.wv[word]
        return np.zeros(128)

    def text2vec(self, text):
        if type(text) is list:
            text = " ".join(text)
        ar = np.array([self.word2vec(t) for t in text.split(" ")])
        return np.mean(ar, axis=0)

    def similarity(self, text1, text2):
        a = self.text2vec(text1)
        b = self.text2vec(text2)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def ranking(self, query, corpus):
        similiars = {i: self.similarity(query, corpus[i]) for i in range(len(corpus))}
        dictionary = {i: corpus[i] for i in range(len(corpus))}
        similiars = sorted(similiars.items(), key=lambda x: -x[1])
        indices = map(lambda x: x[0], similiars)
        print(similiars[:10])
        return [" ".join(dictionary[i]) for i in indices][:10]


# export
embedding = Embedding()
