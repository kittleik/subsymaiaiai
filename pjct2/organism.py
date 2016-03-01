from random import randint

class Organism:

    def __init__(self, dna):
        self.dna = dna
        self.phenotype = self.generatePhenotype()
        self.testScore = None

    def __lt__(self, other):
        return self.testScore > other.testScore

    def generatePhenotype(self):
        phenotype = list(str(self.dna.genotype)[2:])

        for i in range(self.dna.bitsInGenotype-len(phenotype)):
            phenotype.insert(0,'0')

        return phenotype

    def haveSexAndMakeBaby(self, other):
        dnaString = ''
        for i in range(len(self.phenotype)):
            coinFlip = randint(0,1)
            if coinFlip:
                dnaString += self.phenotype[i]
            else:
                dnaString += other.phenotype[i]
                
        return bin(int(dnaString,2))
