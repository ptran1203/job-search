
# Salary estimation based on job description and requirement
# job description and requirement are text, denote as X
# Feed it into neural network, estimate the Salary
# input is vector space (bag of words)
# features:
#     skills
#     requirement
#     description
    
import os
from keras.models import model_from_json, Sequential, Model
from keras.layers import (Dense, Dropout, Activation, Flatten,
                        MaxPooling2D,
                        Input, ZeroPadding2D, BatchNormalization)
from keras.optimizers import Adam
from keras import backend
import numpy as np
# from sklearn.model_selection import train_test_split

MODEL = None
VOCAB = None

DIR = os.path.dirname(os.path.realpath(__file__))

def neural_network(input_tensor):
    model = Sequential()
    model.add(Dense(input_tensor, activation = 'relu'))
    model.add(Dropout(0.3))
    # model.add(Dense(456), activation = 'relu')
    # model.add(Dropout(0.3))
    model.add(Dense(456, activation = 'relu'))
    model.add(Dropout(0.3))
    model.add(Dense(456, activation = 'relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1, activation = 'linear'))
    model.compile(loss='mean_absolute_error',
                optimizer=Adam(lr=1e-4),
                metrics=['mse'])
    return model

def save(model):
    print('Saving the model ...')
    # save model structure
    with open(DIR + '/model.json', "w") as f:
        f.write(model.to_json())
    # save the weights and history
    model.save_weights(DIR + '/model.h5')
    print('done!')

def load_model():
    global MODEL
    json_file = open(DIR + '/model.json', 'r')
    model = json_file.read()
    json_file.close()
    model = model_from_json(model)
    # load weights into new model
    model.load_weights(DIR + '/model.h5')
    MODEL = model
    MODEL._make_predict_function()
    return model


def predict(vector):
    if MODEL is None:
        backend.clear_session()
        load_model()
    
    if MODEL:
        return MODEL.predict([vector])[0]
    
    backend.clear_session()
    load_model()
    return MODEL.predict([vector])[0]

def vocabulary():
    global VOCAB
    if VOCAB:
        return VOCAB
    with open(DIR + '/vocab', 'r') as f:
        VOCAB = f.read().split(',')
    return VOCAB

def get_vector(text):
    vocab = vocabulary()
    vec = [0] * len(vocab)
    for i, word in enumerate(vocab):
        count = text.count(word)
        if count > 0:
            vec[i] += count
    
    print(len(vec))
    return np.asarray(vec)

def load_train():
    trainX = []
    trainY = []
    with open('trainX', 'r') as f:
        trainX = [_.split(',') for _ in f.read().split('-')]
        trainX = [float(_) for _ in trainX]
        trainX = np.asarray(trainX)
    with open('trainY', 'r') as f:
        trainY = np.asarray([float(_) for _ in f.read().split('-')])

    return trainX, trainY

if __name__ == "__main__":
    trainX, trainY = load_train()
    input_tensor = len(trainX[0])
    model = neural_network(input_tensor)
    H = model.fit(x=trainX, y=trainY)
    save(model)


