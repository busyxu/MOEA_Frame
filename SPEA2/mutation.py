import random
from SPEA2 import object_func


def mutation(population, mutation_probability, re):
    size = len(population)
    n = len(population[0].gene)
    m = len(population[0].func)
    for i in range(size):
        t = int(n / 2)
        p = random.uniform(0, 1)
        if p < mutation_probability:
            while t > 0:
                t -= 1
                j = random.randint(0, n-1)
                population[i].gene[j] = random.uniform(0, 1)
                pass
            population[i].func = object_func.f_func(population[i].gene, m, re)
            pass
        pass
    pass


def mutation_pm(population, mutation_pro, eta, re):
    m = len(population[0].func)
    for pop in population:
        p = random.uniform(0, 1)
        if p < mutation_pro:
            u = random.uniform(0, 1)
            if u <= 0.5:
                delta = (2*u)**(1/(eta+1)) - 1
                pass
            else:
                delta = 1-(2*(1-u))**(1/(eta+1))
                pass
            for j in range(len(pop.gene)):
                off = pop.gene[j] + delta
                # if off < 0:
                #     off = 0
                #     pass
                # if off > 1:
                #     off = 1
                #     pass
                if off < 0 or off > 1:
                    continue
                pop.gene[j] = off
                pass
                pop.func = object_func.f_func(pop.gene, m, re)
            pass
        pass
    pass
