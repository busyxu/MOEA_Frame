import numpy as np
from NSGA2 import Individual, object_fun

# 满足变量约束的初始化


def initialization(population_size, n, m, re):
    population = []
    for i in range(population_size):
        gene = np.random.random((n,))
        t = Individual.Individual(gene=gene, func=object_fun.f_func(gene, m, re))
        population.append(t)
        pass
    return population
#
# def init_population(individual_size, m, n1, n2):
#     population = []
#     ca = 0
#     while ca < individual_size:
#         # gene = np.random.randint(5, size=(n1, n2))+1
#         gene = []
#         sample1 = np.array([2, 3, 5])
#         t1 = [sample1[np.random.randint(3, size=(206,))] for i in range(5)]
#         sample2 = np.array([1, 2, 3, 5])
#         t2 = [sample2[np.random.randint(4, size=(206,))] for i in range(6)]
#         sample3 = np.array([2, 4, 5])
#         t3 = [sample3[np.random.randint(3, size=(206,))] for i in range(10)]
#         # gene = np.random.random((n,))
#         gene.extend(t1)
#         gene.extend(t2)
#         gene.extend(t3)
#
#         func = object_fun.f_func(gene, m)
#         t = Individual.Individual(gene=gene, func=func)
#         population.append(t)
#         ca += 1
#         pass
#     return population
