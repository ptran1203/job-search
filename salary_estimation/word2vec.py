import gensim.models
import numpy as np
import json
import datetime
from gensim.test.utils import datapath
from gensim import utils

COR_PATH = "./salary_estimation/storage/corpus.cor"
MODEL_PATH = "./salary_estimation/storage/word2vec_model"


class Embedding:
    def __init__(self):
        self.model = gensim.models.Word2Vec.load(MODEL_PATH)

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


class MyCorpus:
    """An iterator that yields sentences (lists of str)."""

    def __iter__(self):
        for line in open(COR_PATH):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)


if __name__ == "__main__":
    # Step 1: build the corpus
    start = datetime.datetime.now()
    with open("./salary_estimation/storage/temp.json", "r") as f:
        data = json.load(f)

    with open(COR_PATH, "w", encoding="utf-8") as f:
        for job_info in data:
            job_desc, title, _ = job_info
            line = title + " " + job_desc.replace("\n", " ")
            f.write(line + "\n")
    print("Built corpus in {}".format(datetime.datetime.now() - start))

    # Step 2: Build model
    start = datetime.datetime.now()
    model = gensim.models.Word2Vec(sentences=MyCorpus(), size=128)
    print("Train model in {}".format(datetime.datetime.now() - start))

    # Step 3: Save the model
    model.save(MODEL_PATH)


# export
embedding = Embedding()
