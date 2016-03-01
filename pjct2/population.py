from dna import DNA
from organism import Organism
from random import random, sample, randint
from math import sqrt, exp
from copy import deepcopy

class Population:

    def __init__(self, bitsInGenotypes):
        self.bitsInGenotypes = bitsInGenotypes
        self.genotypePopulation = []
        self.developedChildren = []
        self.adultSelection = []
        self.parentSelection = []
        self.T = 10

    def initializeChildPopulation(self, numOfChildren):
        for i in range(numOfChildren):
            self.genotypePopulation.append(DNA.randomGenotype(self.bitsInGenotypes))

    def developGenotypePopulation(self):
        self.developedChildren = []
        for dna in self.genotypePopulation:
            self.developedChildren.append(Organism(dna))

    def testPopulation(self):
        for organism in self.developedChildren:
            self.fitnessTest(organism)

    def fitnessTest(self, organism):
        fitness = 0

        for i in organism.phenotype:
            fitness += int(i)

        organism.testScore = fitness

    def fullGenerationalReplacement(self):
        self.adultSelection = []
        for child in self.developedChildren:
            self.adultSelection.append(child)

    def overProduction(self, numOfAdults):
        self.adultSelection = sorted(self.developedChildren)[:numOfAdults]

    def generationalMixing(self, numOfAdults):
        ffa = self.developedChildren + self.adultSelection
        self.adultSelection = sorted(ffa)[:numOfAdults]

    def fitnessProportonateParentSelection(self, numOfParents):
        self.parentSelection = []
        totalFitness = 0
        wheelOfFortune = []


        for adult in self.adultSelection:
            totalFitness += adult.testScore

        weightedSum = 0
        for adult in self.adultSelection:
            weightedFitness = adult.testScore/totalFitness
            weightedSum += weightedFitness
            wheelOfFortune.append(weightedSum)

        while len(self.parentSelection) < numOfParents:
            parent = self.adultSelection[self.wheelSpin(wheelOfFortune)]
            self.parentSelection.append(parent)

    def sigmaScalingParentSelection(self, numOfParents):
        self.parentSelection = []
        totalFitness = 0
        wheelOfFortune = []


        for adult in self.adultSelection:
            totalFitness += adult.testScore

        mean = totalFitness/float(len(self.adultSelection))
        std = self.standardDeviation(self.adultSelection, mean, len(self.adultSelection))

        weightedSum = 0
        for adult in self.adultSelection:
            weightedFitness = (1 + ((adult.testScore - mean) / (2*std)))
            weightedSum += weightedFitness
            wheelOfFortune.append(weightedSum)

        while len(self.parentSelection) < numOfParents:
            parent = self.adultSelection[self.wheelSpin(wheelOfFortune)]
            self.parentSelection.append(parent)

    def tournamentParentSelection(self, numberOfParents, tournamentSize=40, epsilon=0.1):
        self.parentSelection = []
        bestFitChance = 1 - epsilon

        while len(self.parentSelection) < numberOfParents:
            adultPool = deepcopy(self.adultSelection)
            tournamentParticipants = []

            while len(tournamentParticipants) < tournamentSize:
                pickIndex = randint(0,len(adultPool)-1)
                tournamentParticipants.append(adultPool.pop(pickIndex))

            tournamentParticipants = sorted(tournamentParticipants)
            rnd = random()
            if rnd < bestFitChance:
                self.parentSelection.append(tournamentParticipants[0])
            else:
                pickIndex = randint(1,len(tournamentParticipants)-1)
                self.parentSelection.append(tournamentParticipants[pickIndex])

    def boltzmannParentSelection(self, numOfParents):
        self.parentSelection = []
        totalFitness = 0
        wheelOfFortune = []


        for adult in self.adultSelection:
            totalFitness += adult.testScore

        mean = totalFitness/float(len(self.adultSelection))

        weightedSum = 0
        for adult in self.adultSelection:
            weightedFitness = exp(adult.testScore/float(self.T)) / exp(mean/float(self.T))
            weightedSum += weightedFitness
            wheelOfFortune.append(weightedSum)

        while len(self.parentSelection) < numOfParents:
            parent = self.adultSelection[self.wheelSpin(wheelOfFortune)]
            self.parentSelection.append(parent)

        print (self.T)
        self.T -= self.T/len(self.genotypePopulation)


    def mateSelectedParents(self, numOfChildren):
        self.genotypePopulation = []
        while len(self.genotypePopulation) < numOfChildren:
            male, female = sample(self.parentSelection,2)
            dna = DNA(male.haveSexAndMakeBaby(female),self.bitsInGenotypes)
            self.genotypePopulation.append(dna)

    def wheelSpin(self, wheelOfFortune):
        rnd = random() * wheelOfFortune[-1]
        for i, subRange in enumerate(wheelOfFortune):
            if rnd < subRange:
                return i

    def standardDeviation(self,x,mu,n):
        insideSqrt = 0
        for i in x:
            insideSqrt += (i.testScore - mu) ** 2
        insideSqrt = insideSqrt / float(n)
        return max(0.0001,sqrt(insideSqrt))
