import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import constants
from position import Position

class Player:
    trail = []
    direction = constants.DOWN
    dead = False
    length = 0
    pendingDirection = constants.DOWN

    def __init__(self):
        self.trail = [Position(0,0)]
        self.length = 2
        pass

    def moveRight(self):
        if not self.direction == constants.LEFT:
            self.pendingDirection = constants.RIGHT

    def moveLeft(self):
        if not self.direction == constants.RIGHT:
            self.pendingDirection = constants.LEFT

    def moveUp(self):
        if not self.direction == constants.DOWN:
            self.pendingDirection = constants.UP

    def moveDown(self):
        if not self.direction == constants.UP:
            self.pendingDirection = constants.DOWN

    def update(self):
        oldPosition = self.trail[0]
        newX = oldPosition.x
        newY = oldPosition.y

        if self.pendingDirection == constants.UP and not self.direction == constants.DOWN:
            self.direction = constants.UP
            self.trail[0].direction = constants.UP
        elif self.pendingDirection == constants.DOWN and not self.direction == constants.UP:
            self.direction = constants.DOWN
            self.trail[0].direction = constants.DOWN
        elif self.pendingDirection == constants.LEFT and not self.direction == constants.RIGHT:
            self.direction = constants.LEFT
            self.trail[0].direction = constants.LEFT
        elif self.pendingDirection == constants.RIGHT and not self.direction == constants.LEFT:
            self.direction = constants.RIGHT
            self.trail[0].direction = constants.RIGHT

        if self.direction == constants.UP:
            newY -= 1
        elif self.direction == constants.DOWN:
            newY += 1
        elif self.direction == constants.LEFT:
            newX -= 1
        elif self.direction == constants.RIGHT:
            newX += 1

        newTrail = [Position(newX, newY, self.direction)] + self.trail

        if len(newTrail) > self.length:
            newTrail = newTrail[:-1]

        self.trail = newTrail

    def isCollision(self):
        myPos = self.trail[0]
        otherPoses = self.trail[1:]

        for otherPos in otherPoses:
            if myPos.x == otherPos.x and myPos.y == otherPos.y:
                return True
            elif myPos.x == otherPos.x and myPos.y == otherPos.y:
                return True
            elif myPos.x == otherPos.x and myPos.y == otherPos.y:
                return True
            elif myPos.x == otherPos.x and myPos.y == otherPos.y:
                return True

    def getPos(self):
        return self.trail[0]