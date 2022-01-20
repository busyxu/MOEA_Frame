import sys
import copy
import random
import math
import time


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


def fitness_assignment(population, k):
    m = len(population[0].func)
    for p in population:
        p.S = 0
        for q in population:
            if jude_dominated(p, q):
                p.S += 1
                # P[j].np += 1
                pass
            pass
        pass

    # k = int(math.sqrt(len(P) + len(Q)))
    for pop_i in population:
        dt = []
        pop_i.R = 0
        for pop_j in population:
            if pop_i == pop_j:
                continue
            t = 0
            idx = 0
            while idx < m:
                t += (pop_i.func[idx] - pop_j.func[idx]) ** 2
                idx += 1
                pass
            dt.append(math.sqrt(t))  # i个体到P+Q种群中所有个体的距离

            if jude_dominated(pop_j, pop_i):
                pop_i.R += pop_j.S
                pass
            pass

        dt = sorted(dt)
        pop_i.D = 1/(dt[k]+2)  # 选取第k近
        pop_i.fitness = pop_i.R + pop_i.D
        pass

    pass


class Tuple(object):
    def __init__(self, nd1, nd2, dt):
        self.nd1 = nd1
        self.nd2 = nd2
        self.dt = dt
        pass

    def __str__(self):
        return "nd1:{} nd2:{} dt:{}".format(self.nd1, self.nd2, self.dt)
    pass


def environmental_select(P, Q, M):
    # print(len(P), len(Q))
    P_Q = P + Q
    m = len(P_Q[0].func)
    P_Q_sort = sorted(P_Q, key=lambda individual: individual.fitness)
    # next_P = []
    next_Q = []
    while len(P_Q_sort) > 0:  # 将P和Q中的非支配集加入归档集next_Q中
        if P_Q_sort[0].fitness < 1:
            next_Q.append(P_Q_sort.pop(0))
            pass
        else:
            break
        pass

    while len(next_Q) < M:  # 归档集未满，根据适应度将P_Q中的个体依次加入到next_Q直到M
        pop = P_Q_sort.pop(0)
        next_Q.append(pop)
        pass

    # **************************************************
    # l = len(next_Q)
    # if l > M:
    #     print("*****正在进行剪枝操作，比较耗时(需要剪枝数量为", l-M, ")，请稍等......")
    #     pass
    # t1 = time.time()
    # while len(next_Q) > M:
    #     q_tuple = []
    #     for i, pop1 in enumerate(next_Q):
    #         for j, pop2 in enumerate(next_Q):
    #             if i >= j:
    #                 continue
    #             dt = 0
    #             for idx in range(m):
    #                 dt += math.sqrt((pop1.func[idx] - pop2.func[idx]) ** 2)
    #                 pass
    #             q_tuple.append(Tuple(i, j, dt))
    #             pass
    #         pass
    #     q_tuple = sorted(q_tuple, key=lambda tuple1: tuple1.dt)
    #
    #     # 距离最近的两个点
    #     nd1 = q_tuple[0].nd1
    #     nd2 = q_tuple[0].nd2
    #
    #     for tpl in q_tuple[1:]:
    #         if tpl.nd1 == nd1 or tpl.nd2 == nd1:
    #             del next_Q[nd1]
    #             break
    #         elif tpl.nd1 == nd2 or tpl.nd2 == nd2:
    #             del next_Q[nd2]
    #             break
    #         pass
    #     pass
    # print("剪枝", l-M, "使用时间", time.time()-t1)
    # ------------------------------------------------------------

    # -------------------------下面是剪枝（SPEA2重点）-----------------------
    l = len(next_Q)
    delete_Q = []
    n = l - M
    t1 = time.time()
    if l > M:  # 归档集大于M时，剪枝，依次将next_Q中个体删除 (注意：剪枝过程非常耗时，归档集的大小不能比种群大小小太多)

        # *****************为了提高剪枝速度，把计算距离操作提出来******************
        q_tuple = []
        for i, pop1 in enumerate(next_Q):
            for j, pop2 in enumerate(next_Q):
                if i >= j:
                    continue
                dt = 0
                for idx in range(m):
                    dt += math.sqrt((pop1.func[idx] - pop2.func[idx]) ** 2)
                    pass
                q_tuple.append(Tuple(i, j, dt))
                pass
            pass
        q_tuple = sorted(q_tuple, key=lambda tuple1: tuple1.dt)
        # **************************************************

        # print("*****正在进行剪枝操作，比较耗时(需要剪枝数量为", n, ")，请稍等......")
        while n > 0:
            # 距离最近的两个点
            nd1 = q_tuple[0].nd1
            nd2 = q_tuple[0].nd2

            for tpl in q_tuple[1:]:
                if tpl.nd1 == nd1 or tpl.nd2 == nd1:
                    delete_tuple = []
                    for t in q_tuple:
                        if t.nd1 == nd1 or t.nd2 == nd1:
                            delete_tuple.append(t)  # 记录要删除的tuple
                            # del q_tuple[idx]  # 直接删除的方法会出错，如果有两个需要删除的元素相邻，则后面的不会删除
                            pass
                        pass
                    for tt in delete_tuple:
                        q_tuple.remove(tt)
                        pass

                    delete_Q.append(next_Q[nd1])  # 记录下要删除的个体
                    n -= 1
                    break
                elif tpl.nd1 == nd2 or tpl.nd2 == nd2:
                    delete_tuple = []
                    for t in q_tuple:
                        if t.nd1 == nd2 or t.nd2 == nd2:
                            delete_tuple.append(t)
                            pass
                        pass
                    for tt in delete_tuple:
                        q_tuple.remove(tt)
                        pass

                    delete_Q.append(next_Q[nd2])  # 记录下要删除的个体
                    n -= 1
                    break
                pass

            pass

        for pop in delete_Q:
            next_Q.remove(pop)
            pass

        pass
    # print("剪枝", l-M, "使用时间:", time.time() - t1)
    # ------------------------------------------------------------

    return next_Q


def mating_select(population, population_size):
    mating_pool = []
    size = len(population)  # 归档集大小
    ca = 0
    while ca < population_size:
        ca += 1
        fa = random.randint(0, size-1)  # 闭区间
        ma = random.randint(0, size-1)
        if population[fa].fitness < population[ma].fitness:
            mating_pool.append(copy.deepcopy(population[fa]))
            pass
        else:
            mating_pool.append(copy.deepcopy(population[ma]))
            pass
        pass
    return mating_pool


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