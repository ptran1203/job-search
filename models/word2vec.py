import gensim.models

MODEL = None

class Embedding:
    def __init__(self):
        self.model = gensim.models.Word2Vec.load('storage/word2vec_model')


    def word2vec(self, word):
        if word in self.model.wv.vocab:
            return self.model.wv[word]
        return np.zeros(128)


    def text2vec(self, text):
        if type(text) is list:
            text = " ".join(text)
        ar = np.array([word2vec(self.model, t) for t in text.split(" ")])
        return np.mean(ar, axis=0)

    @staticmethod
    def similarity(text1, text2):
        a = text2vec(text1)
        b = text2vec(text2)
        return np.dot(a, b)/ \
            (np.linalg.norm(a)*np.linalg.norm(b))

    @staticmethod
    def ranking(query, corpus):
        similiars = {i: similarity(query, corpus[i]) for i in range(len(corpus))}
        dictionary = {i:corpus[i] for i in range(len(corpus))}
        similiars = sorted(similiars.items(), key=lambda x: -x[1])
        indices = map(lambda x: x[0], similiars)
        print(similiars[:10])
        return [" ".join(dictionary[i]) for i in indices][:10]


# export
embedding = Embedding()
