# 个体
class Individual(object):
    def __init__(self, gene=[], value=0, fitness=0, func=[]):
        self.gene = gene
        self.value = value
        self.fitness = fitness
        self.func = func
        pass

    def __str__(self):
        return '[gene=%s\nfunc=%s\nvalue=%s fitness=%s]\n' % (self.gene, self.func, self.value, self.fitness)

    __repr__ = __str__

    pass
