from random import randint


class EA:

    def __init__(self, bitsInGenotypes):

        self.bitsInGenotypes = bitsInGenotypes
        genotypes = []

        for i in range(10):
            genotypes.append(bin(randint(0,(2**bitsInGenotypes))))

        a = self.generatePhenotypes(genotypes)

        for i in a:
            print (i)
            print (self.fitnessTest(i))

    def generatePhenotypes(self, genotypes):
        phenotypes = []

        for genotype in genotypes:
            phenotype = list(str(genotype)[2:])

            for i in range(self.bitsInGenotypes-len(phenotype)):
                phenotype.insert(0,'0')

            phenotypes.append((phenotype,genotype))

        return phenotypes

    def fitnessTest(self, genotype):
        fitness = 0

        for i in genotype[0]:
            fitness += int(i)

        return fitness
