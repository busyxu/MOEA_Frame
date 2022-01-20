# import random
import numpy as np
from SPEA2 import Individual, object_func


def initialization(population_size, n, m, re):
    population = []
    for i in range(population_size):
        gene = np.random.random((n,))
        t = Individual.Individual(gene=gene, func=object_func.f_func(gene, m, re))
        population.append(t)
        pass
    return population
