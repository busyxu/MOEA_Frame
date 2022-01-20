# import random
from moead import Individual, object_fun
import math
import numpy as np
import sys
import copy


# ！！！ 序列全排列，且无重复
def perm(sequence):
    t = sequence
    if len(t) <= 1:
        return [t]
    r = []
    for i in range(len(t)):
        if i != 0 and sequence[i - 1] == sequence[i]:
            continue
        else:
            s = t[:i] + t[i + 1:]
            p = perm(s)
            for x in p:
                r.append(t[i:i + 1] + x)
                pass
            pass
        pass
    return r


def random_lambda(m, individual_size):  # m目标数 h参考点数
    h = int(math.sqrt(individual_size*2)) + 1 + 1 + 1 - m + 2
    # print(h)
    num = [0]*h + [1]*(m-1)
    # print(num)
    sequence = perm(num)
    # print(sequence)
    a = len(sequence)
    weight = []
    for sq in sequence:
        t = []
        left = -1
        flag = True
        for i, v in enumerate(sq):
            if v == 1:
                w = (i - left - 1)/h
                if w == 0:
                    flag = False
                    break
                # w = (w-1)/h
                left = i
                t.append(w)
                pass
            pass
        if flag == False:
            continue
        tt = 1-np.sum(t)
        if tt == 0:
            continue
        t.append(tt)
        # nw = (len(sq)-left-1)/h
        # t.append(nw)
        if t not in weight:
            weight.append(t)
            pass

        pass

    # while len(weight) > individual_size:
    #     weight.pop()
    #     # if len(weight) > individual_size:
    #     #     weight.pop(-1)
    #     #     pass
    #     pass

    return weight, len(weight)


def compute_weight_vector_distance(weight, m, t):

    # 计算向量距离矩阵
    weight_dt = np.zeros((len(weight), len(weight)))

    for i, w1 in enumerate(weight):
        for j, w2 in enumerate(weight[i+1:]):
            # if i >= j:
            #     continue
            #     pass
            s = 0
            k = 0
            while k < m:
                s += (w1[k]-w2[k])**2
                k += 1
                pass
            # print(i, j)
            weight_dt[i][j+i+1] = math.sqrt(s)
            weight_dt[j+i+1][i] = weight_dt[i][j+i+1]
            pass
        pass
    # for kk in weight_dt:
    #     print(kk)
    field = [[i for i in range(t)] for j in weight]
    # print(field)
    for i, row in enumerate(weight_dt):
        for j, d in enumerate(row[t:]):  # 初始化的时候默认前t个向量是最近的

            for r, b in enumerate(field[i]):  # 判断向量i领域外的向量是不是有比领域中更近的，是的话将其替换
                if i == b:  # 自己不能和自己比
                    continue
                if d < weight_dt[i][b]:
                    field[i][r] = j+t
                    break
                    pass
                pass
            pass
        pass
    # print(field)
    return field


# 初始化种群
def init_population(weight, individual_size, n, m, re):
    population = []
    ca = 0
    while ca < individual_size:
        # gene = [random.uniform(0, 1) for i in range(n)]
        gene = np.random.random((n,))
        t = Individual.Individual(gene=gene)
        population.append(t)
        ca += 1
        pass
    object_fun.object_function(population, m, re)
    new_population = []
    for w_i, w in enumerate(weight):
        mi = sys.maxsize
        idx = 0
        for pop_i, pop in enumerate(population):
            dt = 0
            for j in range(m):
                dt += (w[j] - pop.func[j]) ** 2
                pass
            dt = math.sqrt(dt)
            if dt < mi:
                mi = dt
                idx = pop_i
                pass
            pass
        new_population.append(copy.deepcopy(population[idx]))
        population.pop(idx)
        pass

    return new_population


def init_reference_point(population, m):
    # 最小化问题
    z = [sys.maxsize]*m
    for pop in population:
        for i in range(m):
            if pop.func[i] < z[i]:
                z[i] = pop.func[i]
                pass
            pass
        pass
    return z


def set_ep():
    ep = []
    return ep


# weight = random_lambda(3, 105)
# print(weight)
# compute_weight_vector_distance(random_lambda(3, 15), 3, 15, 3)

