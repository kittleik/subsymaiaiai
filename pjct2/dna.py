from random import randint

class DNA:

    def __init__(self, genotype, bitsInGenotype):
        self.genotype = genotype
        self.bitsInGenotype = bitsInGenotype

    @classmethod
    def randomGenotype(cls, bitsInGenotype):
        return cls(bin(randint(0,(2**bitsInGenotype)-1)), bitsInGenotype)
