from word2vec_model.data_collection import collect_data, parse


def word2vec(model, word):
    if word in model.wv.vocab:
        return model.wv[word]
    return np.zeros(128)

def text2vec(text):
    if type(text) is list:
        text = " ".join(text)
    ar = np.array([word2vec(model, t) for t in text.split(" ")])
    return np.mean(ar, axis=0)

def similarity(text1, text2):
    a = text2vec(text1)
    b = text2vec(text2)
    return np.dot(a, b)/ \
        (np.linalg.norm(a)*np.linalg.norm(b))


def ranking(query, corpus):
    similiars = {i: similarity(query, corpus[i]) for i in range(len(corpus))}
    dictionary = {i:corpus[i] for i in range(len(corpus))}
    similiars = sorted(similiars.items(), key=lambda x: -x[1])
    indices = map(lambda x: x[0], similiars)
    print(similiars[:10])
    return [" ".join(dictionary[i]) for i in indices][:10]


class Corpus(object):
    def __iter__(self):
        corpus_path = datapath('/content/job_desc.cor')
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)

def train:
    sentences = Corpus()
    model = gensim.models.Word2Vec(sentences=sentences, min_count=5, size=128)

    vec_king = model.wv.similarity('media', 'loai')