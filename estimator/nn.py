
# Salary estimation based on job description and requirement
# job description and requirement are text, denote as X
# Feed it into neural network, estimate the Salary
# input is vector space (bag of words)

from keras.models import model_from_json, Sequential, Model
from keras.layers import (Dense, Dropout, Activation, Flatten,
                        MaxPooling2D,
                        Input, ZeroPadding2D, BatchNormalization)
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split

def neural_network(input_tensor):
    model = Sequential()
    model.add(Dense(input_tensor), activation = 'relu')
    model.add(Dropout(0.3))
    model.add(Dense(456), activation = 'relu')
    model.add(Dropout(0.3))
    model.add(Dense(456), activation = 'relu')
    model.add(Dropout(0.3))
    model.add(Dense(456), activation = 'relu')
    model.add(Dropout(0.3))
    model.add(Dense(1), activation = 'linear')
    model.compile(loss='mean_absolute_error',
                optimizer=Adam(lr=1e-4),
                metrics=['mse'])
    return model


if __name__ == "__main__":
    model = neural_network()
    model.fit()



