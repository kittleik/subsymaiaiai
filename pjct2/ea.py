from random import randint


class EA:

    def __init__(self, ):

        genotypes = []

        for i in range(10):
            genotypes.append(bin(randint(0,(2**10))))

        print (genotypes)
