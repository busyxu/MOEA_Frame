import sys


class Individual(object):
    def __init__(self, dt=sys.maxsize, crowd_dt=0, gene=[], func=[]):
        self.dt = dt
        self.crowd_dt = crowd_dt
        self.gene = gene
        self.func = func
        pass

    def __str__(self):
        return 'gene={}\nfunc={}\ncrowd_dt={} dt={}\n'.format(self.gene, self.func, self.crowd_dt, self.dt)

    __repr__ = __str__
