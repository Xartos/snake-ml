from pygame.locals import *
import pygame
import time
import sys
import random

from snake.snake import Snake
from ml.robot import Robot
from ml.geneticlearn import GeneticLearning

# fix random seed for reproducibility
#np.random.seed(7)

class App:
    windowWidth = 800
    windowHeight = 600
    game = 0
    human = True
    robot = None

    def __init__(self, ml = False):
        self._running = True
        self._display_surf = None
        if ml:
            speed = 10
        else:
            speed = 200
        self.game = Snake(speed)
        self.human = not ml

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('Snake ML')
        self.game.on_init()

        if not self.human:
            self.robot = Robot(100, 1)

        self._running = True

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0,0,255))
        self.game.on_render(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        if not self.human:
            population = 10
            print "Starting population generation...",
            sys.stdout.flush()
            genLearn = GeneticLearning(0, population, 0.001, self.game.height * self.game.width, 1)
            genIndex = 0
            self.robot.network = genLearn.generationWeights[genIndex]
            print "done! starting"
            genLearn.onStart(genIndex)

        while( self._running ):
            pygame.event.pump()

            if self.human:
                keys = pygame.key.get_pressed()
            else:
                gameState = self.game.getGameState()
                keys = self.robot.calculateKey(gameState)

            self.game.update(keys)

            keys = pygame.key.get_pressed()
            if (keys[K_ESCAPE]):
                self._running = False

            if not self.human and (self.game.hasWon() <= 1 or self.game.player.dead):
                genLearn.onComplete(genIndex, self.game.score)

                if genIndex == population - 1:
                    genLearn.onAllComplete(cross = False, createNew=1)
                    genIndex = 0
                    print "All done, scores:"
                    print genLearn.generationResult
                else:
                    genIndex += 1
                self.robot.network = genLearn.generationWeights[genIndex]

                self.game.reset()

                pygame.event.pump()
                keys = pygame.key.get_pressed()
                if (keys[K_ESCAPE]):
                    self._running = False

                genLearn.onStart(genIndex)

            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    ml = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "ml":
            ml = True
    theApp = App(ml=ml)
    theApp.on_execute()