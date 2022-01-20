import numpy as np
import copy
from moead import Individual, object_fun
# from Test_Function import DTLZ
import random
import sys


# 判断非支配个体
def jude_dominated(p, q):
    m = len(p.func)
    # 最小化问题
    i = 0
    flag = True
    cnt = 0
    while i < m:
        if p.func[i] > q.func[i]:
            flag = False
            break
            pass
        elif p.func[i] == q.func[i]:
            cnt += 1
            pass
        i += 1
        pass
    if flag:
        if cnt < m:  # 不能所有目标相等
            return True
        else:
            return False
        pass
    else:  # 存在一个目标不小于则不支配
        return False

    pass


def recombination(n, population, field_i, re):
    k_point = np.random.randint(0, len(field_i))
    l_point = np.random.randint(0, len(field_i))
    k_point = field_i[k_point]
    l_point = field_i[l_point]
    fa_gene = copy.deepcopy(population[k_point].gene)
    ma_gene = copy.deepcopy(population[l_point].gene)
    m = len(population[k_point].func)
    ca = 0
    while ca < n:
        p = np.random.uniform(0, 1)
        if p < 0.5:
            t = fa_gene[ca]
            fa_gene[ca] = ma_gene[ca]
            ma_gene[ca] = t
            pass
        ca += 1
        pass

    fa = Individual.Individual(gene=fa_gene, func=object_fun.f_func(fa_gene, m, re))
    ma = Individual.Individual(gene=ma_gene, func=object_fun.f_func(ma_gene, m, re))
    off_string = copy.deepcopy(ma)
    if jude_dominated(fa, ma):
        off_string = copy.deepcopy(fa)
        pass

    return off_string


def recombination_sbx(population, field_i, eta, re):
    k_point = np.random.randint(0, len(field_i))
    l_point = np.random.randint(0, len(field_i))
    k_point = field_i[k_point]
    l_point = field_i[l_point]
    fa_gene = copy.deepcopy(population[k_point].gene)
    ma_gene = copy.deepcopy(population[l_point].gene)
    m = len(population[k_point].func)
    u = random.uniform(0, 1)
    if u <= 0.5:
        gamma = (2 * u) ** (1 / (eta + 1))
        pass
    else:
        gamma = (1 / (2 * (1 - u))) ** (1 / (eta + 1))
        pass
    fa = population[k_point]
    ma = population[l_point]
    for j in range(len(fa.gene)):
        off1 = 0.5 * ((1 + gamma) * fa.gene[j] + (1 - gamma) * ma.gene[j])
        off2 = 0.5 * ((1 - gamma) * fa.gene[j] + (1 + gamma) * ma.gene[j])
        if off1 < 0 or off1 > 1 or off2 < 0 or off2 > 1:
            continue
        fa_gene[j] = off1
        ma_gene[j] = off2
        pass

    fa = Individual.Individual(gene=fa_gene, func=object_fun.f_func(fa_gene, m, re))
    ma = Individual.Individual(gene=ma_gene, func=object_fun.f_func(ma_gene, m, re))
    off_string = copy.deepcopy(ma)
    if jude_dominated(fa, ma):
        off_string = copy.deepcopy(fa)
        pass

    return off_string


def improvement(off_string, mutation_pro, eta, re):
    m = len(off_string.func)
    p = random.uniform(0, 1)
    if p < mutation_pro:
        u = random.uniform(0, 1)
        if u <= 0.5:
            delta = (2*u)**(1/(eta+1)) - 1
            pass
        else:
            delta = 1-(2*(1-u))**(1/(eta+1))
            pass
        for j in range(len(off_string.gene)):
            off = off_string.gene[j] + delta
            if off < 0 or off > 1:
                continue
            off_string.gene[j] = off
            pass
        pass
    off_string.func = object_fun.f_func(off_string.gene, m, re)
    return off_string


def update_reference_point(off_string, z, m):
    # 最小化问题
    for i in range(m):
        if off_string.func[i] < z[i]:
            z[i] = off_string.func[i]
            pass
        pass
    pass


def weighted_sum_approach(population, off_string, weight, field, i):
    # 权重向量一般经过原点
    for j in field[i]:  # 最开始i向量绑定i个体
        gws_x = np.dot(weight[j], population[j].f)  # 每个领域绑定者的gws
        gws_y = np.dot(weight[j], off_string.f)  # 每个领域的后代gws值
        if gws_y < gws_x:
            population[j] = copy.deepcopy(off_string)
            pass
        pass
    pass


def tchebycheff_approach(population, off_string, weight, field, i, z):
    # 切比雪夫向量经过参考点z

    for j in field[i]:  # 最开始j向量绑定j个体 遍历i领域的个体
        gte_x = 0
        # print("越界:", j)
        for s, w in enumerate(weight[j]):
            # t = w * abs(population[j].func[s] - z[s])
            if w == 0:
                w = 1/sys.maxsize
                pass
            t = abs(population[j].func[s] - z[s]) / w
            # t = w / abs(population[j].func[s] - z[s])
            if t > gte_x:
                gte_x = t
                pass
            pass

        gte_y = 0
        for s, w in enumerate(weight[j]):
            # t = w * abs(off_string.func[s] - z[s])
            if w == 0:
                w = 1/sys.maxsize
                pass
            t = abs(off_string.func[s] - z[s]) / w
            # # t = w / abs(off_string.func[s] - z[s])
            if t > gte_y:
                gte_y = t
                pass
            pass

        if gte_y <= gte_x:
            population[j] = copy.deepcopy(off_string)
            pass

        pass

    pass


def boundary_intersection_approach(population, off_string, weight, field, i, z, theta):
    # 基于惩罚的边界交叉方法

    for j in field[i]:  # 最开始i向量绑定i个体
        dt = np.array(z) - np.array(population[j].func)
        d1 = np.dot(dt, weight[j]) / np.linalg.norm(weight[j])
        d2 = np.linalg.norm(np.array(population[j].func) - (np.array(z) - d1 * np.array(weight[j])))
        gbi_x = d1 + theta*d2

        dt = np.array(z) - np.array(off_string.func)
        d1 = np.dot(dt, weight[j]) / np.linalg.norm(weight[j])
        d2 = np.linalg.norm(np.array(off_string.func) - (np.array(z) - d1 * np.array(weight[j]) / np.linalg.norm(weight[j])))
        gbi_y = d1 + theta * d2

        if gbi_y < gbi_x:
            population[j] = copy.deepcopy(off_string)
            pass
        pass

    pass


def update_ep(off_string, ep, m):
    flag1 = True
    flag2 = True
    for i, pop in enumerate(ep):
        if jude_dominated(off_string, pop):
            # ep.remove(pop)
            del ep[i]
            pass
        if jude_dominated(pop, off_string):
            flag1 = False
            pass
        for j in range(m):
            if pop.func[j] != off_string.func[j]:
                break
            pass
        if j == m-1:
            flag2 = False

        pass
    if flag1 and flag2:
        ep.append(copy.deepcopy(off_string))
        pass
    pass
