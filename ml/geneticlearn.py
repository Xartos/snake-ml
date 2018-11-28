import random
import sys
import time

from network import Network

class GeneticLearning:
    generationWeights = []
    generationResult = []
    generationTime = []
    generation = 0
    mutationRate = 0
    populationSize = 0
    startTime = 0

    gameSize = 0
    additionalFeature = 0

    def __init__(self, generations, populationSize, mutationRate, gameSize, additionalFeature):
        generation = 0
        for i in range(populationSize):
            self.generationWeights += [Network(gameSize, additionalFeature)]
            self.generationResult += [0]
            self.generationTime += [0]

        self.mutationRate = mutationRate
        self.populationSize = populationSize
        self.gameSize = gameSize
        self.additionalFeature = additionalFeature

    def onStart(self, index):
        if index == 0:
            print "Starting gen ", self.generation
        print index,
        sys.stdout.flush()
        self.startTime = time.time()

    def onComplete(self, index, result):
        stopTime = time.time()
        # TODO fix time points
        self.generationResult[index] = result + int((stopTime - self.startTime) * 1000)^2

    def onAllComplete(self, cross = True, createNew = 0):
        ## Add time
        #combinedGeneration = zip(self.generationResult, self.generationWeights)

        selector = []

        print "\nGen complete, creating new...",
        sys.stdout.flush()

        maxVal = 0
        minVal = sys.maxint

        for result in self.generationResult:
            if result > maxVal:
                maxVal = result
            if result < minVal:
                minVal = result

        self.generationResult[:] = [x - minVal for x in self.generationResult]

        for i, result in enumerate(self.generationResult):
            selector += [i] * (result + 1)

        newGenWeights = [0] * self.populationSize
        for i in range(self.populationSize - createNew):
            child = None
            if cross:
                mother = self.generationWeights[random.choice(selector)]
                father = self.generationWeights[random.choice(selector)]
                child = mother.combine(father)
            else:
                parent = self.generationWeights[random.choice(selector)]
                child = parent.mutate(0.01)
            newGenWeights[i] = child

        for i in range(self.populationSize - createNew, self.populationSize):
            newGenWeights[i] = Network(gameSize=self.gameSize, additionalFeature=self.additionalFeature) # Add new random

        print "done"

        self.generationWeights = newGenWeights
        self.generation += 1