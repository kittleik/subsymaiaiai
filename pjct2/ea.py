from population import Population

class EA:

    def __init__(self ,numOfGenerations, numOfChildren, numOfAdults, numOfParents, bitsInGenotypes, fitnessMethod, adultSelectionMethod, parentSelectionMethod):

        self.numOfGenerations = numOfGenerations
        self.numOfChildren = numOfChildren
        self.numOfAdults = numOfAdults
        self.numOfParents = numOfParents
        self.pop = Population(bitsInGenotypes)
        self.adultSelectionMethod = adultSelectionMethod
        self.parentSelectionMethod = parentSelectionMethod

        self.pop.initializeChildPopulation(self.numOfChildren)

        self.startEvolution()

    def startEvolution(self):
        for generation in range(self.numOfGenerations):
            self.pop.developGenotypePopulation()
            self.pop.testPopulation()

            fitnessSum = 0
            for c in self.pop.developedChildren:
                fitnessSum += c.testScore
            print(generation)
            print(fitnessSum)

            self.adultSelection()
            self.parentSelection()
            self.pop.mateSelectedParents(self.numOfChildren)

    def adultSelection(self):
        if self.adultSelectionMethod == 0:
            self.pop.fullGenerationalReplacement()
        if self.adultSelectionMethod == 1:
            self.pop.overProduction(self.numOfAdults)
        if self.adultSelectionMethod == 2:
            self.pop.generationalMixing(self.numOfAdults)

    def parentSelection(self):
        if self.parentSelectionMethod == 0:
            self.pop.fitnessProportonateParentSelection(self.numOfParents)
        if self.parentSelectionMethod == 1:
            self.pop.sigmaScalingParentSelection(self.numOfParents)
        if self.parentSelectionMethod == 2:
            self.pop.tournamentParentSelection(self.numOfParents)
        if self.parentSelectionMethod == 3:
            self.pop.boltzmannParentSelection(self.numOfParents)
