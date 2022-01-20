class Individual(object):
    def __init__(self, S=0, R=0, D=0, fitness=0, func=[], gene=[]):
        self.S = S
        self.R = R
        self.D = D
        self.fitness = fitness
        self.func = func
        self.gene = gene
        pass

    def __str__(self):
        # print(self.gene)
        # print(self.func)
        return '[gene=%s\nfunc=%s\nfitness=%s\nS=%s\nR=%s\nD=%s]\n' % (self.gene, self.func, self.fitness, self.S, self.R, self.D)

    __repr__ = __str__
    pass
