import pickle
import numpy as np
from salary_estimation.word2vec import embedding


class salaryEsimator:
    def __init__(self):
        self.model = pickle.load(open("./salary_estimation/storage/model.pkl", "rb"))
        self.max_val = pickle.load(open("./salary_estimation/storage/maxval.pkl", "rb"))

    def predict(self, feat):
        if len(feat.shape) == 1:
            feat = np.expand_dims(feat, 0)
        return self.model.predict(feat) * self.max_val

    def predict_from_text(self, text):
        feat = embedding.text2vec(text)
        return self.predict(feat)


salary_estimator = salaryEsimator()
