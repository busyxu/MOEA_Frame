import sys
import copy
import random
import functools
import numpy as np


def jude_dominating(p, q):
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


def fast_sort(population):
    s = {}
    n = {}
    f = []
    pt = []  # 记录一层非支配层
    for p in population:
        st = []  # p支配的个体
        nt = 0  # 支配p的个体数
        for q in population:
            if jude_dominating(p, q):
                st.append(q)
                pass
            elif jude_dominating(q, p):
                nt += 1
                pass
            pass
        # s[p.idx] = st  # 第i个个体所支配的个体集合
        s[id(p)] = st
        # n[p.idx] = nt  # 支配的第i个个体的个体数
        n[id(p)] = nt
        if nt == 0:  # 没有个体支配p
            pt.append(p)
            pass
        pass
    f.append(pt)
    i = 0
    while len(f[i]) > 0:  # 由于判断条件，会多一个空层
        pt = []
        for p in f[i]:
            # for q in s[p.idx]:  # q下一层支配，则-1
            for q in s[id(p)]:  # q下一层支配，则-1
                n[id(q)] -= 1
                # n[q.idx] -= 1
                # if n[q.idx] == 0:  # 不存在支配q的个体，则加入当前层
                if n[id(q)] == 0:  # 不存在支配q的个体，则加入当前层
                    pt.append(q)
                    pass
                pass
            pass
        i += 1
        f.append(pt)
        pass
    f.pop()
    return f


def sequential_search_strategy(p, f):
    x = len(f)  # 已经被分配的支配层数
    k = 0  # 当前检索的层
    while True:
        flag = False
        for q in reversed(f[k]):
            if jude_dominating(q, p):
                flag = True
                break
                pass
            pass
        if flag:  # p 被f[k]中的个体支配
            k += 1
            if k >= x:
                t = []
                f.append(t)
                # return x + 1
                x += 1
                f[k].append(p)
                break
                pass
            pass

        else:  # p 不被f[k]中的个体支配
            # return k
            f[k].append(p)
            break
            pass

        pass
    pass


def binary_search_strategy(p, f):
    x = len(f)  # 已经找到的支配层数
    k_min = 0  # 检索的最底层
    k_max = x  # 检索的最高层
    # k = int(np.floor((k_max+k_min)/2 + 1/2))  # 当前检索的层
    k = int((k_max+k_min)/2)
    while True:
        flag = False
        for q in reversed(f[k]):
            if jude_dominating(q, p):
                flag = True
                break
                pass
            pass

        if flag:  # k小了，要往上层走，直到k==k_max-1
            # k_min = k  # k层能支配p 需要判断高层是否有支配p的。
            if (k == k_max-1) and (k_max < x):  # k是支配p的直接上一层
                # return k_max
                f[k_max].append(p)
                break
                pass
            elif k == x-1:  # 已存在的最后一层(k)支配p,则需要新加入一层
                # return x+1
                # x += 1
                t = []
                f.append(t)
                f[x].append(p)
                x += 1
                break
                pass
            else:  # k层能支配p 但不是直接支配p的一层 需要判断高层是否有支配p的。
                # k = np.floor((k_max + k_min)/2 + 1/2)
                k_min = k
                k = int((k_max + k_min)/2)
                pass
            pass

        else:  # k大了，要往下层走，直到k==k_min+1
            if k == k_min:  # 当k==k_min 说明k是不能支配p的最小一层(就是说比k小的层通通支配p)
                # return k
                f[k].append(p)
                break
                pass
            else:  # k层不能支配p 但不是最小的层 需要往下层走。
                k_max = k
                k = int((k_max+k_min)/2)
                pass
            pass

        pass
    pass


def nd_sort(a):  # a是一个pop_size*m大小的矩阵
    # a = pop.obj_fun
    pop = copy.deepcopy(a)
    m = len(pop[0].func)
    a = np.zeros((len(pop), m))
    for i, p in enumerate(pop):
        for j, f in enumerate(p.func):
            a[i][j] = f
            pass
        pass

    N = a.shape[0]  # 得到第一个维度的大小，即总群大小
    front = np.full(N, -1, dtype=np.int32)  #

    index = np.lexsort(np.rot90(a))
    # ans = []
    MaxFNo = 0
    for i in index:
        NowFNo = 0
        while True:
            Dominated = False
            for j in np.flipud(np.where(front == NowFNo)[0]):
                # if jude_dominating(a[j], a[i]):
                if jude_dominating(pop[j], pop[i]):
                    Dominated = True
                    break
            if Dominated:
                NowFNo += 1
                if NowFNo > MaxFNo:
                    MaxFNo += 1
            else:
                front[i] = NowFNo
                break
    ans = []
    for i in range(MaxFNo+1):
        ans.append([])
    # ans = np.empty((MaxFNo+1,))
    for k, ft in enumerate(front):
        ans[ft].append(copy.deepcopy(pop[k]))
        # ans[ft] = 1
    # print(ans)
    return ans


def cmp(pop1, pop2):
    m = len(pop1.func)
    i = 0
    while i < m:
        if pop1.func[i] < pop2.func[i]:
            return -1
        elif pop1.func[i] > pop2.func[i]:
            return 1
        else:
            i += 1
            # return 0
            pass
        pass
    return 0


def ens_ss(population):

    f = [[]]
    # population_sort = sorted(population, key=lambda individual: individual.f1)
    # print(population)
    population_sort = sorted(population, key=functools.cmp_to_key(cmp))
    # print(population_sort)
    for pop in population_sort:
        # sequential_search_strategy(pop, f)
        binary_search_strategy(pop, f)
        pass
    return f


def crowding_distance_assigment(population):
    m = len(population[0].func)
    f_max = [population[0].func[i] for i in range(m)]
    f_min = [population[0].func[i] for i in range(m)]
    for pop in population:
        pop.crowd_dt = 0

        for j in range(m):
            if pop.func[j] > f_max[j]:
                f_max[j] = pop.func[j]
                pass
            if pop.func[j] < f_min[j]:
                f_min[j] = pop.func[j]
                pass
            pass

        pass
    # print(f_max)
    # print(f_min)

    for i in range(m):
        population = sorted(population, key=lambda individual: individual.func[i])
        population[0].crowd_dt = sys.maxsize
        population[-1].crowd_dt = sys.maxsize
        for idx, pop in enumerate(population[1:-2]):
            pop.crowd_dt = pop.crowd_dt + abs(population[idx + 1].func[i] - population[idx - 1].func[i])/(f_max[i]-f_min[i])
            pass
        pass

    pass


def best_individual(population):
    best_pop = copy.deepcopy(population[0])
    for pop in population:
        if jude_dominating(pop, best_pop):
            best_pop = copy.deepcopy(pop)
            pass

        # if best_pop.fitness > pop.fitness:
        #     best_pop = copy.deepcopy(pop)
        #     pass

        pass
    return best_pop


# 更新种群
def select_population(population, population_size):

    new_population = []
    # best_pop = best_individual(population, m)
    # new_population.append(best_pop)
    # ca = 1
    ca = 0
    while ca < population_size:
        fa_idx = random.randint(0, population_size-1)
        ma_idx = random.randint(0, population_size-1)
        if fa_idx == ma_idx:
            continue
        fa = copy.deepcopy(population[fa_idx])
        ma = copy.deepcopy(population[ma_idx])
        if jude_dominating(fa, ma):
            new_population.append(fa)
            pass
        else:
            if fa.crowd_dt > ma.crowd_dt:
                new_population.append(fa)
                pass
            else:
                new_population.append(ma)
                pass
            pass

        # if fa.fitness < ma.fitness:
        #     new_population.append(fa)
        #     pass
        # else:
        #     new_population.append(ma)

        ca += 1
    return new_population
