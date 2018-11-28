import numpy as np
from pygame.locals import *

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import constants
from network import Network

class Robot:
    network = None

    def __init__(self, gameSize, additionalFeature):
        self.network = Network(gameSize, additionalFeature)

    def calculateKey(self, gameState):
        keys = [False] * 323 # Length of pygame.key.get_pressed()

        headCoord = None
        tail = []
        direction = constants.DOWN
        # Get direction
        for i in range(gameState.shape[0]):
            for j in range(gameState.shape[1]):
                if gameState[i, j] == constants.HEAD:
                    headCoord = (i, j)

        for i in range(gameState.shape[0]):
            for j in range(gameState.shape[1]):
                if gameState[i, j] == constants.BODY:
                    tail += [(i, j)]

        if len(tail) > 0:
            almostHead = tail[-1]
            almostHeadX = almostHead[0]
            almostHeadY = almostHead[1]
            headX = headCoord[0]
            headY = headCoord[1]
            if almostHeadX == headX - 1:
                direction = constants.RIGHT
            elif almostHeadX == headX + 1:
                direction = constants.LEFT
            elif almostHeadY == headY + 1:
                direction = constants.UP
            elif almostHeadY == headY - 1:
                direction = constants.DOWN

        gameStateArray = gameState.flatten()

        # Append additional features
        gameStateArray = np.matrix(np.append(np.asarray(gameStateArray), np.array(direction)))

        predictions = self.network.model.predict(gameStateArray)
        max = 0
        index = 0
        for prediction in predictions:
            for i, value in enumerate(prediction):
                if value > max:
                    index = i
                    max = value

        if index == 0:
            keys[K_UP] = True
        elif index == 1:
            keys[K_DOWN] = True
        elif index == 2:
            keys[K_RIGHT] = True
        elif index == 3:
            keys[K_LEFT] = True

        return keys

def isWallRight(direction, headCoord, gamestate):
    if direction != None:
        if direction == constants.DOWN and headCoord[0] == 0:
            return True
        elif direction == constants.RIGHT and headCoord[1] == gameState.shape[1] - 1:
            return True
        elif direction == constants.UP and headCoord[0] == gameState.shape[0] - 1:
            return True
        elif direction == constants.LEFT and headCoord[1] == 0:
            return True
    return False

def isWallLeft(direction, headCoord, gamestate):
    if direction != None:
        if direction == constants.DOWN and headCoord[0] == gameState.shape[0] - 1:
            return True
        elif direction == constants.RIGHT and headCoord[1] == 0:
            return True
        elif direction == constants.UP and headCoord[0] == 0:
            return True
        elif direction == constants.LEFT and headCoord[1] == gameState.shape[1] - 1:
            return True
    return False

def isWallAhead(direction, headCoord, gamestate):
    if direction != None:
        if direction == constants.DOWN and headCoord[1] == gameState.shape[1] - 1:
            return True
        elif direction == constants.RIGHT and headCoord[0] == gameState.shape[0] - 1:
            return True
        elif direction == constants.UP and headCoord[1] == 0:
            return True
        elif direction == constants.LEFT and headCoord[0] == 0:
            return True
    return False