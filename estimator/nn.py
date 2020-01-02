
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
    vector = np.expand_dims(vector, axis=0)
    if MODEL:
        return MODEL.predict(vector)[0][0]
    
    backend.clear_session()
    load_model()
    return MODEL.predict(vector)[0][0]

def vocabulary():
    global VOCAB
    if VOCAB:
        return VOCAB
    with open(DIR + '/vocab', 'r') as f:
        VOCAB = f.read().split(',')
    return VOCAB

def get_vector(text, isnp = True):
    rate = 5
    vocab = vocabulary()
    vec = [0] * len(vocab)
    for i, word in enumerate(vocab):
        count = text.count(word)
        if count > 0:
            vec[i] += count

    vec = [sum(vec[n:n + rate]) for n in range(0, len(vec), rate)]
    if isnp:
        return np.asarray(vec)
    return ','.join([str(_) for _ in vec])

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
    # trainX, trainY = load_train()
    # input_tensor = len(trainX[0])
    # model = neural_network(input_tensor)
    # H = model.fit(x=trainX, y=trainY)
    # save(model)
    txt = " Work with QA Lead to perform quality assurance of company world-class internet products. - Cooperate with Business Analytics, Product Owners to test and certify software code that is aligned to the software testing and development standards and principles, leveraging common testing solutions and services in an Agile/ Scrum methodology. - Report to QA Lead. # Benefits for this position: - Working hours from 9am - 6pm, Monday - Friday; - 13th month bonus; - Annual salary increment. - Premium healthcare insurance; - Weekly Sports activities; - Monthly, Quarterly engagement activities; - Summer outing and company trip; - 15 annual leave days per year; - OT and standby support allowance (if any); - Free fruits and tea break in the office; - Friendly working environment with young and dynamic team; - Advancement/ promotion prospects. - Working location: 3rd floor, VOV Building, 07 Nguyen Thi Minh Khai, Ben Nghe Ward, District 1, Ho Chi Minh City # Manual skill set: - Requirement analysis - Test plan (team and individually), test case, test execution - Exploratory testing # Automation skill set: - Selenium/ Appium - Cucumber - Java - Maven. # Working experience - 3-5 years - Experienced working in a product company - Experienced working in a scrum team - Experienced testing on mobile - Experience desktop web app Senior QA QC Engineer"
    v = get_vector(txt)
    # v = [0,0,0,0,0,26,0,0,0,0,0,0,1,0,3,0,1,0,0,0,0,0,0,1,0,0,0,3,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,3,1,1,0,0,0,0,0,0,0,0,0,0,6,0,2,0,0,0,39,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,5,0,0,0,0,23,2,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,102,4,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,4,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,5,0,0,0,1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2,0,0,0,1,0,0,0,4,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,4,0,0,1,15,13,0,0,0,0,0,6,0,0,0,1,0,0,0,0,0,0,0,1,0,2,0,0,0,1,0,0,0,3,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,7,1,0,0,0,0,0,0,3,0,0,1,0,0,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,6,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,3,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,0,0,3,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,4,0,0,0,0,2,0,0,0,0,7,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,4,0,0,0,2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,13,0,0,0,1,0,1,0,0,0,0,0,2,0,0,3,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,2,0,0,0,1,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,1,3,0,7,0,0,0,0,0,0,0,1,0,0,2,0,0,9,0,0,0,0,0,0,0,1,0,0,0,0,0,0,9,0,0,0,0,0,0,6,1,0,0,0,0,2,0,0,0,0,0,1,0,0,0,0,2,0,0,0,0,5,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,3,0,0,0,11,0,0,0,4,0,0,1,1,0,0,0,0,3,0,0,1,0,0,5,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,7,0,2,0,1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3,0,2,0,0,0,0,23,0,0,0,0,0,0,3,0,0,0,0,0,6,0,0,0,0,0,1,0,0,0,4,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,6,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2,1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,43,0,0,2,0,0,0,0,0,2,0,0,0,0,0,2,0,3,0,0,0,0,0,0,4,1,0,2,0,0,0,0,0,0,0,6,0,5,0,0,0,2,1,0,0,0,0,2,0,0,0,0,0,37,0,0,0,0,0,0,6,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,89,0,1,0,11,0,0,0,0,0,0,0,0,0,3,0,1,0,0,0,1,0,1,0,1,6,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2,3,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,5,0,0,60,2,0,0,0,0,0,0,3,0,3,0,3,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,17,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,5,0,0,2,1,4,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0]
    print(predict(np.asarray(v)))

