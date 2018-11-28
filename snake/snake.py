import numpy as np
from pygame.locals import *
import pygame
from datetime import datetime, timedelta
import random

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import constants
from player import Player
from position import Position

class Snake:
    blockSize = 32
    height = 10
    width = 10
    score = 0
    player = 0

    snakeImage = None

    # Snek Body
    snakeImageLeftRight = None
    snakeImageUpDown = None
    snakeImageUpRight = None
    snakeImageUpLeft = None
    snakeImageDownRight = None
    snakeImageDownLeft = None
    # Snek Head
    snakeHeadDown = None
    snakeHeadUp = None
    snakeHeadLeft = None
    snakeHeadRight = None
    appleImage = None
    lastUpdate = datetime.now()
    apple = 0
    speed = 0
    won = False
    updatesSinceLast = 0
    fps = 0.0

    def __init__(self, speed = 200):
        self.player = Player()
        self.apple = self.getRandomPos()
        self.speed = speed

    def hasWon(self):
        nBlocks = self.height * self.width
        if self.player.length == nBlocks:
            self.won = True
        return nBlocks - self.player.length

    def getRandomPos(self):
        foundUnique = False
        posProposal = None
        if self.hasWon() <= 1:
            return None
        while not foundUnique:
            posProposal = Position(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            foundOne = False
            for pos in self.player.trail:
                if pos.x == posProposal.x and pos.y == posProposal.y:
                    foundOne = True
            if not foundOne:
                foundUnique = True

        return posProposal

    def on_init(self):
        self.snakeImage = pygame.image.load("resources/images/snake.png").convert()
        self.snakeImageLeftRight = pygame.image.load("resources/images/leftRight.png").convert_alpha()
        self.snakeImageUpDown = pygame.image.load("resources/images/upDown.png").convert_alpha()

        self.snakeImageUpLeft = pygame.image.load("resources/images/upLeft.png").convert_alpha()
        self.snakeImageUpRight = pygame.image.load("resources/images/upRight.png").convert_alpha()
        self.snakeImageDownLeft = pygame.image.load("resources/images/downLeft.png").convert_alpha()
        self.snakeImageDownRight = pygame.image.load("resources/images/downRight.png").convert_alpha()

        self.snakeHeadDown = pygame.image.load("resources/images/downHead.png").convert_alpha()
        self.snakeHeadUp = pygame.image.load("resources/images/upHead.png").convert_alpha()
        self.snakeHeadRight = pygame.image.load("resources/images/rightHead.png").convert_alpha()
        self.snakeHeadLeft = pygame.image.load("resources/images/leftHead.png").convert_alpha()
        self.appleImage = pygame.image.load("resources/images/apple.png").convert_alpha()

    def on_render(self, display):
        font = pygame.font.SysFont('Courier 10 Pitch', 20)

        # Render map
        for xBlock in range(self.width + 1):
            pygame.draw.line(display, (0, 0, 0), (xBlock * self.blockSize, 0), (xBlock * self.blockSize, self.height * self.blockSize))
        for yBlock in range(self.height + 1):
            pygame.draw.line(display, (0, 0, 0), (0, yBlock * self.blockSize), (self.width * self.blockSize, yBlock * self.blockSize))

        if self.won:
            textsurface = font.render("You won!! Your score: " + str(self.score) + " press \"R\" to reset", False, (255, 0, 0))
            display.blit(textsurface, (20, (self.blockSize * self.height) + 20))

        if self.player.dead:
            textsurface = font.render("You're DEAD!! Your score: " + str(self.score) + " press \"R\" to reset", False, (255, 0, 0))
            display.blit(textsurface, (20, (self.blockSize * self.height) + 20))

        # Render snake
        for i, pos in enumerate(self.player.trail):
            isLast = (i == (len(self.player.trail) - 1))
            # Head
            if i == 0:
                if pos.direction == constants.UP:
                    display.blit(self.snakeHeadUp, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.DOWN:
                    display.blit(self.snakeHeadDown, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.LEFT:
                    display.blit(self.snakeHeadLeft, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.RIGHT:
                    display.blit(self.snakeHeadRight, (pos.x * self.blockSize, pos.y * self.blockSize))
            elif isLast:
                if pos.direction == constants.UP or pos.direction == constants.DOWN:
                    display.blit(self.snakeImageUpDown, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.LEFT or pos.direction == constants.RIGHT:
                    display.blit(self.snakeImageLeftRight, (pos.x * self.blockSize, pos.y * self.blockSize))
                else:
                    display.blit(self.snakeImage, (pos.x * self.blockSize, pos.y * self.blockSize))
            else:
                # Body
                nextDirection = self.player.trail[i + 1].direction
                if pos.direction == constants.RIGHT and nextDirection == constants.UP:
                    display.blit(self.snakeImageDownRight, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.RIGHT and nextDirection == constants.DOWN:
                    display.blit(self.snakeImageUpRight, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.LEFT and nextDirection == constants.UP:
                    display.blit(self.snakeImageDownLeft, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.LEFT and nextDirection == constants.DOWN:
                    display.blit(self.snakeImageUpLeft, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.UP and nextDirection == constants.LEFT:
                    display.blit(self.snakeImageUpRight, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.UP and nextDirection == constants.RIGHT:
                    display.blit(self.snakeImageUpLeft, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.DOWN and nextDirection == constants.LEFT:
                    display.blit(self.snakeImageDownRight, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.DOWN and nextDirection == constants.RIGHT:
                    display.blit(self.snakeImageDownLeft, (pos.x * self.blockSize, pos.y * self.blockSize))

                elif pos.direction == constants.UP or pos.direction == constants.DOWN:
                    display.blit(self.snakeImageUpDown, (pos.x * self.blockSize, pos.y * self.blockSize))
                elif pos.direction == constants.LEFT or pos.direction == constants.RIGHT:
                    display.blit(self.snakeImageLeftRight, (pos.x * self.blockSize, pos.y * self.blockSize))
                else:
                    display.blit(self.snakeImage, (pos.x * self.blockSize, pos.y * self.blockSize))

        if not self.apple == None:
            display.blit(self.appleImage, (self.apple.x * self.blockSize, self.apple.y * self.blockSize))

        # Render score
        textsurface = font.render("score: " + str(self.score), False, (255, 255, 255))
        display.blit(textsurface,((self.blockSize * self.width) + 10, self.blockSize / 2 - 10))

        textsurface = font.render("FPS: " + str(self.fps), False, (255, 255, 255))
        display.blit(textsurface,((self.blockSize * self.width) + 10, self.blockSize / 2 + 10))


    def isDeadNextTime(self):
        pos = self.player.getPos()
        direction = self.player.pendingDirection
        if direction == constants.UP and pos.y == 0:
            return True
        if direction == constants.DOWN and pos.y == self.height - 1:
            return True
        if direction == constants.LEFT and pos.x == 0:
            return True
        if direction == constants.RIGHT and pos.x == self.width - 1:
            return True

        return False

    def isOnApple(self):
        if self.apple == None:
            return False
        pos = self.player.getPos()
        return (pos.x == self.apple.x) and (pos.y == self.apple.y)

    def reset(self):
        self.player = Player()
        self.score = 0
        self.won = False
        self.apple = self.getRandomPos()

    def update(self, keys):
        if (keys[K_RIGHT]):
            self.player.moveRight()

        if (keys[K_LEFT]):
            self.player.moveLeft()

        if (keys[K_UP]):
            self.player.moveUp()

        if (keys[K_DOWN]):
            self.player.moveDown()

        if (self.player.dead or self.won) and keys[K_r]:
            self.reset()

        self.updatesSinceLast += 1
        if datetime.now() > self.lastUpdate + timedelta(milliseconds=self.speed) and not self.player.dead and not self.won:
            if self.isDeadNextTime():
                self.player.dead = True
                return

            self.player.update()
            self.lastUpdate = datetime.now()

            if self.player.isCollision():
                self.player.dead = True
                return

            if self.isOnApple():
                self.apple = self.getRandomPos()
                self.score += 1
                self.player.length += 1

            self.fps = self.updatesSinceLast * (1000.0 / self.speed)
            self.updatesSinceLast = 0

    def getGameState(self):
        gameState = np.matrix([[constants.FREE] * self.height] * self.width)

        gameState[self.apple.x, self.apple.y] = constants.APPLE

        trail = self.player.trail
        head = trail[0]
        gameState[head.x, head.y] = constants.HEAD

        body = trail[1:]

        for part in body:
            gameState[part.x, part.y] = constants.BODY

        return gameState