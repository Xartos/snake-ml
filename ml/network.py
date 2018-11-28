import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense

class Network:
    weights = [None, None]
    layers = [None, None]
    model = None

    def __init__(self, gameSize = None, additionalFeature = None, weights = None):
        if (gameSize == None or additionalFeature == None) and weights == None:
            print "Cannot initialize a network with neither network size or weights"
            return None
        if weights == None:
            weights = [None, None]
            weights[0] = [np.random.rand(gameSize + additionalFeature, 12) * 2 - 1, np.random.rand(12) * 2 - 1]
            weights[1] = [np.random.rand(12, 4) * 2 - 1, np.random.rand(4) * 2 - 1]

        self.setWeights(weights)

    def setWeights(self, weights):
        # Create model
        self.model = Sequential()
        self.layers[0] = Dense(12, input_dim=weights[0][0].shape[0], activation='relu')
        self.model.add(self.layers[0])
        self.layers[1] = Dense(4, activation='softmax')
        self.model.add(self.layers[1])
        self.layers[0].set_weights(weights[0])
        self.layers[1].set_weights(weights[1])
        self.weights = weights

        # Compile model
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def mutate(self, mutationRate):

        for i, weight in enumerate(self.weights):
            for j, innerWeight in enumerate(weight):
                for k, innerInnerWeight in enumerate(innerWeight):
                    if random.random() <= mutationRate:
                        if type(innerInnerWeight) is np.ndarray:
                            for l in range(len(innerInnerWeight)):
                                self.weights[i][j][k][l] = random.random() * 2 - 1
                        elif type(innerInnerWeight) is np.float64:
                            self.weights[i][j][k] = random.random() * 2 - 1

        # Recompile network
        self.setWeights(self.weights)
        return self

    def combine(self, other, mutationRate = 0.001):
        weightLen = self.weights[0][0].shape[0]
        newWeights = [[None, None], [None, None]]

        newWeights[0][0] = np.append(self.weights[0][0][weightLen / 2:], other.weights[0][0][:weightLen / 2], axis=0)
        newWeights[0][1] = np.append(self.weights[0][1][12 / 2:], other.weights[0][1][:12 / 2], axis=0)
        newWeights[1][0] = np.append(self.weights[1][0][12 / 2:], other.weights[1][0][:12 / 2], axis=0)
        newWeights[1][1] = np.append(self.weights[1][1][4 / 2:], other.weights[1][1][:4 / 2], axis=0)

        return Network(weights = newWeights).mutate(mutationRate)