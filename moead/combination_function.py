import numpy as np


def weighted_sum_approach(population, Lambda):
    g_ws = []
    for i, pop in enumerate(population):
        t = np.dot(Lambda[i], pop.func)
        g_ws.append(t)
        pass

    pass

#
# a = [1, 2, 3, 4, 5]
# b = [1, 2, 3, 4, 5]
# print(np.dot(a, b))
